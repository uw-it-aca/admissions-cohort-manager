<template>
  <b-container>
    <b-row class="aat-cohort-manager">
      <b-col cols="5" sm="auto" class="aat-main-navbar">
        <header>
          <div class="aat-app-info">
            <div class="aat-app-name">Admissions Assignment Tool</div>
            <div class="aat-user-netid">Welcome user.netid</div>
          </div>
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
      </b-col>
      <b-col>
        <main>
          <h1>this is the wrapper app</h1>
          <router-view />
        </main>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
  export default {};
</script>

<style lang="scss">
  @import '../css/_variables.scss';
  @import '../css/custom.scss';

  .aat-main-navbar {
    background-color: $nav-bkgnd;
    height: 100%;
    padding: 8pt;
  }

  .aat-cohort-manager {
    height: 100vh;
    padding: 16pt;
  }

</style>
