const responseBox = document.getElementById('response-box');
const ticketsContainer = document.getElementById('tickets');
const ticketTemplate = document.getElementById('ticket-card-template');

function showResponse(title, payload) {
  responseBox.textContent = `${title}\n\n${JSON.stringify(payload, null, 2)}`;
}

async function request(url, options = {}) {
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    showResponse(`Error ${response.status}`, payload);
    throw new Error(payload?.detail || `Request failed: ${response.status}`);
  }

  return payload;
}

function renderTicket(ticket) {
  const clone = ticketTemplate.content.cloneNode(true);
  const card = clone.querySelector('article');

  clone.querySelector('.ticket-title').textContent = `${ticket.title} (${ticket.id.slice(0, 8)})`;
  clone.querySelector('.ticket-meta').textContent = `status: ${ticket.status} | priority: ${ticket.priority}`;
  clone.querySelector('.ticket-description').textContent = ticket.description;
  clone.querySelector('.ticket-tags').textContent = `tags: ${ticket.tags.join(', ') || 'none'}`;

  const commentInput = clone.querySelector('.comment-input');
  const commentBtn = clone.querySelector('.comment-btn');
  const assigneeInput = clone.querySelector('.assignee-input');
  const assignBtn = clone.querySelector('.assign-btn');
  const transitionSelect = clone.querySelector('.transition-select');
  const transitionBtn = clone.querySelector('.transition-btn');

  commentBtn.addEventListener('click', async () => {
    const body = commentInput.value.trim();
    if (!body) return;
    try {
      const updated = await request(`/tickets/${ticket.id}/comments`, {
        method: 'POST',
        body: JSON.stringify({ author: 'ui.user', body }),
      });
      commentInput.value = '';
      showResponse('Comment added', updated);
      await loadTickets();
    } catch (error) {
      showResponse('Comment failed', { message: error.message });
    }
  });

  assignBtn.addEventListener('click', async () => {
    const assignee = assigneeInput.value.trim();
    if (!assignee) return;
    try {
      const updated = await request(`/tickets/${ticket.id}/assign`, {
        method: 'POST',
        body: JSON.stringify({ assignee }),
      });
      assigneeInput.value = '';
      showResponse('Ticket assigned', updated);
      await loadTickets();
    } catch (error) {
      showResponse('Assign failed', { message: error.message });
    }
  });

  transitionBtn.addEventListener('click', async () => {
    const target_status = transitionSelect.value;
    try {
      const updated = await request(`/tickets/${ticket.id}/transition`, {
        method: 'POST',
        body: JSON.stringify({ target_status }),
      });
      showResponse('Ticket transitioned', updated);
      await loadTickets();
    } catch (error) {
      showResponse('Transition failed', { message: error.message });
    }
  });

  ticketsContainer.append(card);
}

async function loadTickets() {
  ticketsContainer.innerHTML = '';
  const statusFilter = document.getElementById('status-filter').value;
  const query = statusFilter ? `?status=${encodeURIComponent(statusFilter)}` : '';

  try {
    const tickets = await request(`/tickets${query}`);
    if (!tickets.length) {
      ticketsContainer.innerHTML = '<p>No tickets found.</p>';
      return;
    }
    tickets.forEach(renderTicket);
  } catch {
    ticketsContainer.innerHTML = '<p>Failed to load tickets.</p>';
  }
}

document.getElementById('create-ticket-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = event.currentTarget;

  const payload = {
    title: form.title.value.trim(),
    description: form.description.value.trim(),
    reporter: form.reporter.value.trim(),
    priority: form.priority.value,
    assignee: form.assignee.value.trim() || null,
    tags: form.tags.value
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean),
  };

  try {
    const created = await request('/tickets', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    showResponse('Ticket created', created);
    form.reset();
    form.priority.value = 'medium';
    await loadTickets();
  } catch (error) {
    showResponse('Create failed', { message: error.message });
  }
});

document.getElementById('refresh-tickets').addEventListener('click', loadTickets);
document.getElementById('status-filter').addEventListener('change', loadTickets);

document.getElementById('integration-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const ticketId = document.getElementById('integration-ticket-id').value.trim();
  const action = document.getElementById('integration-action').value;

  if (!ticketId) return;

  const pathByAction = {
    jira: `/integrations/jira/sync/${ticketId}`,
    github: `/integrations/github/create-issue/${ticketId}`,
    testrail: `/integrations/testrail/push/${ticketId}`,
  };

  const url = pathByAction[action];

  try {
    const result = await request(url, { method: 'POST' });
    showResponse('Integration response', result);
  } catch (error) {
    showResponse('Integration call result', { message: error.message });
  }
});

loadTickets();
