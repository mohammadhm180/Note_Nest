  function loadNotesByCategory(categoryId) {
    fetch(`/get_notes/${categoryId}`) // Assuming you have a Django view that returns notes based on category
      .then(response => response.json())
      .then(data => {
        var notesList = document.getElementById('notes-list');
            notesList.innerHTML = '';
          data.forEach(note => {
          var noteDiv = document.createElement('div');
          noteDiv.innerHTML = `<a href="notes/note_detail/${note.id}/">
            <div class="note-box">
              <div class="note">
                <div class="title">${note.title}</div>
                <div class="category">دسته بندی : ${note.category}</div>
                <div class="content">${note.text}</div>
              </div>
            </div>
          </a>`;
          notesList.appendChild(noteDiv);
        });
      });
  }

  loadNotesByCategory(0);

  document.getElementById('category-select').addEventListener('change', function() {
    var categoryId = this.value;
    loadNotesByCategory(categoryId);
  });