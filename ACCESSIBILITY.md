# Accessibility

Nexus Revoluter berkomitmen biar semua Pioneer bisa pakai, termasuk yang pakai keyboard saja, screen reader, atau HP kentang dengan koneksi lemot.

Akses itu bagian dari amanah. Kalau satu Pioneer gak bisa akses, berarti kita belum sovereign beneran.

## Priorities

Kami prioritaskan:

- Semua fungsi utama bisa dioperasikan pakai keyboard saja, tanpa mouse
- Semua halaman terbaca rapi oleh screen reader seperti TalkBack di Android dan VoiceOver di iOS
- Layout responsif untuk mobile, tablet, dan desktop
- Kontras warna cukup dan teks tidak bergantung pada warna saja
- Bahasa sederhana, tersedia dalam Bahasa Indonesia dan English

Target kami adalah WCAG 2.2 Level AA sebagai tujuan aspirasional. Kami belum klaim sudah tersertifikasi, kami terus evaluasi tiap rilis.

## Contributor expectations

Setiap kontribusi yang mengubah UI wajib:

- Pakai HTML semantik, button untuk aksi, link untuk navigasi
- Tambahkan aria-label untuk ikon dan aksi tanpa teks
- Pastikan semua elemen interaktif bisa dijangkau pakai Tab dan Shift Tab
- Test manual: coba operasikan flow utama cuma pakai keyboard
- Sertakan screenshot atau rekaman kalau ada perubahan visual

## Reporting accessibility issues

Kalau lo nemu barrier, lapor lewat GitHub Issues.

Sertakan info ini kalau bisa:

- Halaman atau URL yang bermasalah
- Apa yang lo coba lakukan
- Browser, OS, dan assistive technology yang lo pakai
- Screenshot atau rekaman layar kalau ada

Lo tidak perlu menjelaskan kondisi medis atau disabilitas lo.

## Severity

- **Kritis**: Fitur utama gak bisa dipakai sama sekali pakai keyboard atau screen reader
- **Mayor**: Satu flow penting terhambat, tapi ada workaround
- **Minor**: Masalah kecil, tidak menghalangi tugas utama

## How we respond

- Kami akui laporan dalam 3 hari kerja
- Kami kasih status dan perkiraan waktu perbaikan
- Kami kasih workaround sementara kalau ada
- Kami kabari pelapor kalau fix sudah live buat diverifikasi

## Ownership and maintenance

- Owner: KOSASIH, maintainer utama nexus-revoluter
- Accessibility di-review tiap ada rilis besar dan tiap ada perubahan UI utama
- Kalau ownership pindah, akan diumumkan di Discussions dan dicatat di file ini

## Supported environments

Kami test di:

- Android: Chrome terbaru, TalkBack aktif
- iOS: Safari terbaru, VoiceOver aktif
- Desktop: Chrome, Firefox, Edge versi terbaru
- Input: touch, mouse, keyboard saja
- Koneksi: 3G lemot dan offline sebagian untuk halaman statis

Kombinasi di luar daftar di atas belum kami evaluasi penuh, tapi tetap boleh dilaporkan.
