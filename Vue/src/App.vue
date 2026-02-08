<template>
  <div>
    <h1>Social Feed</h1>

    <nav>
      <router-link to="/">Feed</router-link> |
      <router-link to="/create">Create</router-link>
    </nav>

    <router-view />
  </div>
</template>