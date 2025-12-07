const modal = document.getElementById('contact-modal');
const openBtn = document.getElementById('open-modal-btn');
const closeBtn = document.getElementById('close-modal-btn');

// Open the modal
openBtn.addEventListener('click', () => {
  modal.showModal(); // Using showModal() creates the backdrop automatically
});

// Close the modal
closeBtn.addEventListener('click', () => {
  modal.close();
});

// Optional: Close if clicking on the backdrop (outside the modal)
modal.addEventListener('click', (event) => {
  const rect = modal.getBoundingClientRect();
  const isInDialog = (rect.top <= event.clientY && event.clientY <= rect.top + rect.height
    && rect.left <= event.clientX && event.clientX <= rect.left + rect.width);
  if (!isInDialog) {
    modal.close();
  }
});