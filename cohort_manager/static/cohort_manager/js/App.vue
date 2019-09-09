<template>
  <b-container fluid>
    <b-row class="aat-cohort-manager">
      <b-col cols="4" lg="2" class="aat-main-navbar">
        <header>
          <div class="aat-app-info">
            <a href="/" class="aat-app-name">Admissions Assignment Tool</a>
            <div class="aat-user-netid">Welcome user.netid</div>
          </div>
          <b-nav vertical class="aat-nav-group">
            <b-link to="/cohort/" class="nav-link">
              Assign Cohort
            </b-link>
            <b-link to="/major/" class="nav-link">
              Assign Major
            </b-link>
          </b-nav>
          <b-nav vertical class="aat-nav-group">
            <b-link to="/log/" class="nav-link">
              Activity Log
            </b-link>
          </b-nav>
          <b-nav vertical class="aat-link-group">
            <b-link href="https://www.tableau.com" class="nav-link" target="_blank">
              Tableau Selection Tool
            </b-link>
          </b-nav>
        </header>
      </b-col>
      <b-col cols="6" sm="8" lg="10" class="aat-content-area">
        <main>
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

  .aat-page-header {
    font-size: 1.5rem;
    font-weight: bold;
    padding: 24px 0;
  }

  .aat-sub-header {
    color: $sub-header;
    font-size: 1rem;
    font-weight: normal;
    text-transform: uppercase;    
  }

  .aat-app-name {
    color: inherit;
    font-size: 1.5rem;
    line-height: 1.2;

    &:hover {
      text-decoration: none;
    }

  }

  .aat-main-navbar {
    background-color: $nav-bkgnd;
    height: 100%;
    padding: 16pt;
  }

  .aat-app-info {
    margin-bottom: 16px;
  }

  .aat-nav-group {
    margin: 24px 0 0;
  }

  .aat-link-group {
    border-top: solid 1px #666;
    margin-top: 16px;
    padding-top: 8px;
  }

  .aat-cohort-manager {
    height: 100vh;
  }

  div.aat-content-area {
    padding: 0 48px;
  }

  .aat-form-section {
    margin: 0 0 3rem;
  }

</style>
