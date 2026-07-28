# StampOne Decoder

A Django web app that detects and decodes invisible watermarks (steganographic messages) embedded in photos, using the **StampOne v89** model (256-bit message, AttentionVNet architecture). Built by [VisTeam, ISR-UC](https://visteam.isr.uc.pt/home). Project docs: https://farhadsh1992.github.io/StampOne/

## What it does

You give it a photo containing a StampOne-encoded region (a face, an object, a QR-style pattern, or a pink-bordered area). The app:

1. Runs a detector to locate the encoded region in the photo (Face Detection, Object Detection, Pink Border, or QR Code Pattern).
2. Crops that region and feeds it to the StampOne decoder (a TFLite AttentionVNet model).
3. Decodes the embedded 256-bit message and shows it back to you, alongside the original photo and the detected region.

## How to use it

1. Open the app — you'll land on the StampOne splash screen. Tap the logo to continue.
2. On the decoder page, either:
   - **Take Photo** — opens your device/webcam camera live, with a shutter button to capture.
   - **Choose from Gallery** — pick an existing image file.
3. Pick a **Detector** matching how the message was encoded (Face Detection is the default).
4. Tap **Decode Image**. The page shows:
   - The original encoded image and the cropped detected region, side by side.
   - The decoded **Message** (highlighted green on success, red if nothing could be decoded).
   - A status line with detector/decoder diagnostics.

## Running it locally

This app depends on TensorFlow 2.15, OpenCV, and a few other native packages, so it's easiest to run inside a dedicated Conda environment.

```bash
conda env create -f environment.yml
conda activate stampone_dec_001

python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in a browser.

See [help_running.text](help_running.text) for background on why this project needs its own environment (the original `venv/` in this repo was built on a different machine and won't run as-is).

### Configuration (for deployment)

`core/settings.py` reads `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` from environment variables (via a `.env` file, loaded with `python-dotenv`), falling back to the original insecure dev defaults when unset — so local runs need no setup. Before deploying publicly:

1. Copy `.env.example` to `.env`.
2. Generate a real secret key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
3. Set `DJANGO_SECRET_KEY` to that value, `DJANGO_DEBUG=False`, and `DJANGO_ALLOWED_HOSTS` to your real domain(s).

`.env` is gitignored — never commit real secrets.

### Model files

Two large model files (the StampOne decoder `.tflite` weights and the PRNet face-detection weight file) are **not included in this repository** — they exceed GitHub's 100MB file size limit. To run the app, place your own copies at:

- `Tools_stega89_de1/tfLite_stampone89_deocder/StampOne_decoder_v89_infl32_float32.tflite`
- `Tools_stega89_de1/tfLite_stampone89_deocder/StampOne_decoder_v89_intfl32_float16.tflite`
- `DetectionLibs/Tools_Face_Detection_System/net-data/256_256_resfcn256_weight.data-00000-of-00001` (and the matching copies under `DetectionLibs/.../DataPrnet/net-data/` and `FarhadCV/Face_Detection_Utilies/Data/net-data/`)

## Tech stack

- Django 5.0, TensorFlow 2.15 / Keras 2.15, OpenCV
- Vanilla JS for camera capture (`getUserMedia`) and gallery upload — no external camera SDK
- Bootstrap 5 for layout
