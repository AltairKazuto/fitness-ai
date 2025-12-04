<template>
  <div id="app">
    <!-- Navigation -->
    <nav>
      <router-link to="/">Home</router-link>
      |
      <router-link to="/dashboard">Dashboard</router-link>
    </nav>

    <!-- Where the routed component will appear -->
    <router-view />
  </div>
</template>

<script setup lang="ts">
// No need to import Home/Dashboard here
// The router handles which component to show
</script>

<style>
nav {
  margin-bottom: 20px;
}
nav a {
  text-decoration: none;
  color: blue;
  margin-right: 10px;
}
nav a.router-link-exact-active {
  font-weight: bold;
  color: darkblue;
}
</style>