<template>
  <div class="cohort_manager">
    <header>
      <nav>
        <div>
          <router-link to="/" class="nav-link">
            Landing Page
          </router-link>
          <router-link to="/upload/" class="nav-link">
            Import
          </router-link>
          <router-link to="/cohort/" class="nav-link">
            Cohort View
          </router-link>
          <router-link to="/log/" class="nav-link">
            Log View
          </router-link>
        </div>
      </nav>
    </header>

    <main>
      <h1>this is the wrapper app</h1>
      <router-view />
    </main>
  </div>
</template>

<script>
  export default {};
</script>

<style lang="scss">
@import '../css/custom.scss'


</style>
