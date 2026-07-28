document.addEventListener('DOMContentLoaded', () => {
  const cameraBtn = document.getElementById('cameraBtn');
  const galleryBtn = document.getElementById('galleryBtn');
  const galleryInput = document.getElementById('galleryInput');
  const imageFileInput = document.getElementById('imageFileInput');

  const previewWrap = document.getElementById('previewWrap');
  const previewImage = document.getElementById('previewImage');
  const fileNameLabel = document.getElementById('fileNameLabel');
  const clearBtn = document.getElementById('clearBtn');

  const decodeBtn = document.getElementById('decodeBtn');
  const decodeForm = document.getElementById('decodeForm');
  const loadingOverlay = document.getElementById('loadingOverlay');

  const cameraModal = document.getElementById('cameraModal');
  const cameraVideo = document.getElementById('cameraVideo');
  const cameraCanvas = document.getElementById('cameraCanvas');
  const cameraError = document.getElementById('cameraError');
  const cameraCancelBtn = document.getElementById('cameraCancelBtn');
  const cameraCaptureBtn = document.getElementById('cameraCaptureBtn');
  const cameraSwitchBtn = document.getElementById('cameraSwitchBtn');

  function setSelectedFile(file) {
    if (!file) return;

    const transfer = new DataTransfer();
    transfer.items.add(file);
    imageFileInput.files = transfer.files;

    previewImage.src = URL.createObjectURL(file);
    fileNameLabel.textContent = file.name;
    previewWrap.classList.remove('d-none');
    decodeBtn.disabled = false;
  }

  galleryBtn.addEventListener('click', () => galleryInput.click());
  galleryInput.addEventListener('change', (e) => setSelectedFile(e.target.files[0]));

  clearBtn.addEventListener('click', () => {
    imageFileInput.value = '';
    galleryInput.value = '';
    previewWrap.classList.add('d-none');
    previewImage.src = '';
    decodeBtn.disabled = true;
  });

  decodeForm.addEventListener('submit', () => {
    decodeBtn.disabled = true;
    decodeBtn.textContent = 'Decoding...';
    loadingOverlay.classList.remove('d-none');
  });

  // --- Live camera capture (works on mobile browsers and on a MacBook's webcam) ---

  let mediaStream = null;
  let videoDevices = [];
  let currentDeviceId = null;

  function showCameraError(text) {
    cameraError.textContent = text;
    cameraError.classList.remove('d-none');
  }

  function stopCameraStream() {
    if (mediaStream) {
      mediaStream.getTracks().forEach((track) => track.stop());
      mediaStream = null;
    }
  }

  function closeCamera() {
    stopCameraStream();
    cameraModal.classList.add('d-none');
  }

  async function openCamera(deviceId) {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      alert('Camera access needs a secure connection (HTTPS or localhost). Use "Choose from Gallery" instead.');
      return;
    }

    stopCameraStream();
    cameraError.classList.add('d-none');
    cameraModal.classList.remove('d-none');

    const constraints = {
      video: deviceId ? { deviceId: { exact: deviceId } } : { facingMode: { ideal: 'environment' } },
      audio: false,
    };

    try {
      mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
    } catch (err) {
      try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      } catch (err2) {
        showCameraError('Could not access the camera: ' + err2.message);
        return;
      }
    }

    cameraVideo.srcObject = mediaStream;
    const track = mediaStream.getVideoTracks()[0];
    currentDeviceId = track.getSettings().deviceId || null;

    if (!videoDevices.length) {
      const devices = await navigator.mediaDevices.enumerateDevices();
      videoDevices = devices.filter((d) => d.kind === 'videoinput');
      if (videoDevices.length > 1) {
        cameraSwitchBtn.classList.remove('d-none');
      }
    }
  }

  cameraBtn.addEventListener('click', () => openCamera());
  cameraCancelBtn.addEventListener('click', closeCamera);

  cameraSwitchBtn.addEventListener('click', () => {
    if (videoDevices.length < 2) return;
    const idx = videoDevices.findIndex((d) => d.deviceId === currentDeviceId);
    const next = videoDevices[(idx + 1) % videoDevices.length];
    openCamera(next.deviceId);
  });

  cameraCaptureBtn.addEventListener('click', () => {
    if (!mediaStream) return;
    cameraCanvas.width = cameraVideo.videoWidth;
    cameraCanvas.height = cameraVideo.videoHeight;
    cameraCanvas.getContext('2d').drawImage(cameraVideo, 0, 0, cameraCanvas.width, cameraCanvas.height);
    cameraCanvas.toBlob((blob) => {
      if (!blob) return;
      const file = new File([blob], `capture-${Date.now()}.jpg`, { type: 'image/jpeg' });
      setSelectedFile(file);
      closeCamera();
    }, 'image/jpeg', 0.92);
  });

  window.addEventListener('beforeunload', stopCameraStream);
});
