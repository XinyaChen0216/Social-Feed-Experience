<script setup>
import { ref } from "vue";
import api from "@/services/api";

const text = ref("");
const files = ref([]);
const isSubmitting = ref(false);
const errorMsg = ref("");
const successMsg = ref("");

function handleFileChange(e) {
  files.value = Array.from(e.target.files || []);
}

function validateFiles(selected) {
  const allowedImages = ["image/jpeg", "image/png", "image/webp"];
  const allowedVideos = ["video/mp4", "video/quicktime"]; // mp4, mov
  
  const maxImage = 10 * 1024 * 1024;
  const maxVideo = 50 * 1024 * 1024;

  for (const f of selected) {
    const isImage = allowedImages.includes(f.type);
    const isVideo = allowedVideos.includes(f.type);

    if (!isImage && !isVideo) {
      return `Unsupported file type: ${f.name}`;
    }
    if (isImage && f.size > maxImage) {
      return `Image too large (max 10MB): ${f.name}`;
    }
    if (isVideo && f.size > maxVideo) {
      return `Video too large (max 50MB): ${f.name}`;
    }
  }
  return "";
}

async function submitPost() {
  errorMsg.value = "";
  successMsg.value = "";

  const validationError = validateFiles(files.value);
  if (!text.value.trim() && files.value.length === 0) {
    errorMsg.value = "Please add text or at least one file.";
    return;
  }
  if (validationError) {
    errorMsg.value = validationError;
    return;
  }

  isSubmitting.value = true;
  try {
    const formData = new FormData();
    formData.append("text", text.value);

    for (const f of files.value) {
      formData.append("files", f); // must match Django: request.FILES.getlist("files")
    }

    await api.post("/posts/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    text.value = "";
    files.value = [];
    successMsg.value = "Posted!";
  } catch (err) {
    errorMsg.value = err?.response?.data?.detail || "Upload failed";
    console.error(err);
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div style="max-width: 720px; margin: 0 auto; padding: 16px;">
    <h2>Create Post</h2>

    <textarea
      v-model="text"
      placeholder="Write something..."
      rows="4"
      style="width: 100%; padding: 10px; margin-top: 8px;"
    />

    <div style="margin-top: 12px;">
      <input type="file" multiple accept="image/*,video/mp4,video/quicktime" @change="handleFileChange" />
      <div v-if="files.length" style="margin-top: 8px; font-size: 14px;">
        <div v-for="f in files" :key="f.name">• {{ f.name }}</div>
      </div>
    </div>

    <button
      @click="submitPost"
      :disabled="isSubmitting"
      style="margin-top: 12px;"
    >
      {{ isSubmitting ? "Posting..." : "Submit" }}
    </button>

    <p v-if="errorMsg" style="color: red; margin-top: 10px;">{{ errorMsg }}</p>
    <p v-if="successMsg" style="color: green; margin-top: 10px;">{{ successMsg }}</p>
  </div>
</template>

