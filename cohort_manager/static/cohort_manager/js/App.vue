<template>
  <b-container fluid>
    <b-row class="aat-cohort-manager">
      <b-col cols="5" sm="4" md="3" class="aat-main-navbar">
        <header>
          <div class="aat-app-info">
            <div class="aat-app-name">Admissions Assignment Tool</div>
            <div class="aat-user-netid">Welcome user.netid</div>
          </div>
          <b-nav vertical>
            <div class="aat-nav-group">
              <b-link to="/" class="nav-link">
                Home
              </b-link>
              <b-link to="/log/" class="nav-link">
                Activity Log
              </b-link>
            </div>
            <div class="aat-nav-group">
              <b-link to="/cohort/" class="nav-link">
                Assign Cohort
              </b-link>
              <b-link to="/major/" class="nav-link">
                Assign Major
              </b-link>
            </div>
            <div class="aat-link-group">
              <b-link href="https://www.tableau.com" class="nav-link" target="_blank">
                Tableau Selection Tool
              </b-link>
            </div>
          </b-nav>
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

  .aat-app-name {
    font-size: 1.5rem;
  }

  .aat-main-navbar {
    background-color: $nav-bkgnd;
    height: 100%;
    padding: 16pt;
  }

  .aat-nav-group {
    margin: 24px 0;
  }

  .aat-link-group {
    border-top: solid 1px #666;
    padding-top: 16px;
  }

  .aat-cohort-manager {
    height: 100vh;
  }

</style>
