document.addEventListener('DOMContentLoaded', function(){
  const fileInput = document.getElementById('fileInput');
  const uploadBtn = document.getElementById('uploadBtn');
  const status = document.getElementById('uploadStatus');
  const filesDiv = document.getElementById('files');
  const summaryDiv = document.getElementById('summary');

  uploadBtn.addEventListener('click', async () => {
    if (!fileInput.files.length) {
      status.textContent = 'Choose a file first.';
      return;
    }
    const fd = new FormData();
    fd.append('file', fileInput.files[0]);
    status.textContent = 'Uploading...';
    try {
      const res = await fetch('/upload', { method: 'POST', body: fd });
      const j = await res.json();
      if (!res.ok) { status.textContent = 'Upload error: ' + (j.error||res.status); return; }
      status.textContent = 'Uploaded: ' + j.filename;
      // call organize
      filesDiv.textContent = 'Organizing...';
      const orgRes = await fetch('/organize', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ filename: j.filename })});
      const orgJ = await orgRes.json();
      if (!orgRes.ok) { filesDiv.textContent = 'Organize error: ' + (orgJ.error||orgRes.status); return; }
      renderFiles(orgJ);
    } catch (err) {
      status.textContent = 'Network error: ' + err.message;
    }
  });

  function renderFiles(list){
    summaryDiv.textContent = '';
    if (!list || !list.length) { filesDiv.textContent = 'No organized files found.'; return; }
    filesDiv.innerHTML = '';
    list.forEach(fn => {
      const btn = document.createElement('button');
      btn.textContent = 'Summarize ' + fn;
      btn.className = 'btn';
      btn.addEventListener('click', () => summarize(fn));
      filesDiv.appendChild(btn);
    });
  }

  async function summarize(filename){
    summaryDiv.textContent = 'Summarizing...';
    try {
      const res = await fetch('/summarize', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ book_filename: filename }) });
      const j = await res.json();
      if (!res.ok) { summaryDiv.textContent = 'Summarize error: ' + (j.error||j.message||res.status); return; }
      summaryDiv.innerHTML = '';
      const pre = document.createElement('pre');
      pre.textContent = j.summary || j;
      summaryDiv.appendChild(pre);
    } catch (err){
      summaryDiv.textContent = 'Network error: ' + err.message;
    }
  }
});