# Transfer Sentimen Kalimat Menggunakan Reinforcement Learning with Human Feedback
Author: Adzka Ahmadetya Zaidan - 13520127

## Model File Download Link
https://drive.google.com/drive/folders/14YhdXFskd4ALGly8mn1BGH0Zpo_VdnjL?usp=sharing

### Introduction
Repositori ini berisi kode dan data untuk proyek yang berfokus pada penggunaan model Transformer untuk transfer sentimen dengan teknik RLHF. Program ini terbagi ke dalam beberapa tahap, termasuk fine-tuning, reward training, dan policy training menggunakan Proximal Policy Optimization (PPO).

### Struktur Folder
- dataset/: Berisi dataset yang digunakan untuk pelatihan dan evaluasi. -- Dataset yang digunakan adalah ulasan Amazon dan Yelp yang sudah ditranslate
- inferences/: Menyimpan hasil inferensi yang dihasilkan oleh model.
- 0-dataset preparation/: Berisi skrip untuk menyiapkan dataset yang digunakan dalam proses pelatihan, termasuk pembagian dataset.
- 1-sft.ipynb: Notebook Jupyter untuk Fine-Tuning pada model.
- 2-rt.ipynb: Notebook Jupyter untuk Reward Training, yang berfokus pada fine-tuning reward model berdasarkan feedback manusia berbentuk chosen response vs rejected response.
- 3-ppo.ipynb: Notebook Jupyter untuk pelatihan model menggunakan Proximal Policy Optimization (PPO).
- 4-demo.ipynb: Notebook Jupyter yang mendemonstrasikan model secara manual, model yang digunakan dapat disesuaikan.

### Penggunaan Program
1. Instalasi Dependensi: Pastikan untuk menginstal semua library Python yang diperlukan dan dependensi yang diperlukan
2. Siapkan Dataset: Gunakan notebook atau skrip dalam folder 0-dataset preparation untuk menyiapkan dataset yang diperlukan untuk pelatihan.
3. Lakukan Fine-Tuning: Jalankan notebook 1-sft.ipynb untuk melakukan fine-tuning pada model transformer dengan dataset yang telah disiapkan. --> Menghasilkan Fine-Tuned Model
4. Lakukan Inferensi untuk 4-way comparison dan pilih output terbaik dengan format x, y0, y1, y2, y3, b sesuai dengan contoh pada dataset.
5. Lakukan Reward Training: Gunakan notebook 2-rt.ipynb untuk melakukan fine-tuning pada reward model. --> Menghasilkan Reward Model
6. Optimasi dengan PPO: Terakhir, gunakan notebook 3-ppo.ipynb untuk menerapkan teknik reinforcement learning pada fine-tuned model menggunakan PPO. Menerima Fine-Tuned Model + Reward Model --> RLHF Model
7. Demonstrasi Model: Jalankan notebook 4-demo.ipynb untuk mencoba melakukan inferensi secara manual pada model.

### Penyesuaian untuk Model Lain yang Digunakan
- PEFT (Parameter-Efficient Fine-Tuning): Untuk melatih model dengan teknik PEFT, sesuaikan parameter-parameter pada PEFTConfig dengan model yang digunakan jika tersedia.
- PPO: Beberapa penamaan parameter dan fungsi custom khususnya bagian WithValueHead perlu disesuaikan dengan model yang sedang digunakan
- Alternatif Fine-Tuning: Sebagai alternatif, dapat digunakan SFTTrainer dari huggingface untuk proses fine-tuning awal sebelum melanjutkan ke tahap PPO.
