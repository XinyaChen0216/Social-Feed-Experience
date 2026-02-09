<script setup>
import { onMounted, ref } from "vue";
import api from "@/services/api";

const posts = ref([]);
const loading = ref(false);
const errorMsg = ref("");

function isVideo(url) {
  return url?.toLowerCase().endsWith(".mp4") || url?.toLowerCase().endsWith(".mov");
}

async function loadPosts() {
  errorMsg.value = "";
  loading.value = true;
  try {
    const res = await api.get("/posts/");
    posts.value = res.data;
  } catch (err) {
    console.error(err);
    errorMsg.value = "Failed to load feed";
  } finally {
    loading.value = false;
  }
}

const API_BASE = import.meta.env.VITE_API_BASE_URL;

const mediaUrl = (url) => {
  if (!url) return "";
  if (url.startsWith("http")) return url; 
  return `${API_BASE}${url}`;
};

onMounted(loadPosts);
</script>

<template>
  <div style="max-width: 720px; margin: 0 auto; padding: 16px;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <h2>Feed</h2>
      <button @click="loadPosts" :disabled="loading">
        {{ loading ? "Refreshing..." : "Refresh" }}
      </button>
    </div>

    <p v-if="errorMsg" style="color:red;">{{ errorMsg }}</p>
    <p v-if="loading && !posts.length">Loading...</p>

    <div v-for="post in posts" :key="post.id" style="border:1px solid #ddd; padding:12px; border-radius:8px; margin-top:12px;">
      <div style="font-size:14px; color:#666;">
        Post #{{ post.id }} • {{ new Date(post.created_at).toLocaleString() }}
      </div>

      <div v-if="post.text" style="margin-top:8px; white-space:pre-wrap;">
        {{ post.text }}
      </div>

      <!-- Media -->
      <div v-if="post.media?.length" style="margin-top:10px;">
        <!-- images grid -->
        <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:8px;">
          <template v-for="m in post.media" :key="m.id">
            <div v-if="m.media_type === 'image'">
              <img
                :src="mediaUrl(m.url)"
                alt="uploaded"
                loading="lazy"
                style="width:100%; border-radius:8px; object-fit:cover;"
              />
            </div>

            <div v-else-if="m.media_type === 'video'">
              <video controls preload="metadata" style="width:100%; border-radius:8px;">
                <source :src="mediaUrl(m.url)" />
              </video>
            </div>

            <!-- fallback if your API didn't set media_type -->
            <div v-else>
              <video v-if="isVideo(m.url)" controls preload="metadata" style="width:100%; border-radius:8px;">
                <source :src="mediaUrl(m.url)" />
              </video>
              <img v-else :src="mediaUrl(m.url)" alt="uploaded" loading="lazy" style="width:100%; border-radius:8px;" />
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>
