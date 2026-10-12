# ORBIT — aturan kerja

## Knowledge graph (graphify)
- **Sebelum mengubah kode**: baca `graphify-out/GRAPH_REPORT.md` dan/atau query graph (`/graphify query ...`) untuk memahami bagian yang akan disentuh.
- **Setelah setiap perubahan kode/dokumen**: jalankan `/graphify --update` sampai `graphify-out/` (graph.json, GRAPH_REPORT.md, graph.html) ikut diperbarui, lalu commit bersama perubahannya.
- Folder data peserta & biner dikecualikan lewat `.graphifyignore` — jangan dimasukkan ke graph.
