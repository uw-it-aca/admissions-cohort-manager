<template>
  <b-container fluid>
    <b-row class="aat-app-banner">
      <b-col cols="4" lg="2">
        Welcome, <span id="netid">{{ netid }}</span>
      </b-col>
      <b-col cols="8" lg="10">
        <a href="/saml/logout" class="aat-logout-link">Sign out</a>
      </b-col>
    </b-row>
    <b-row class="aat-cohort-manager">
      <b-col cols="4" lg="2" class="aat-main-navbar">
        <header>
          <div class="aat-app-info">
            <a href="/" class="aat-brand-link">
              <img class="aat-app-logo" src="/static/cohort_manager/img/W-Logo.png" alt="UW-IT">
              <span class="aat-app-name">Application Assignment Tool</span>
            </a>
          </div>
          <b-nav vertical class="aat-nav-group">
            <b-link to="/cohort/" class="aat-button btn btn-secondary">
              Assign Cohort
            </b-link>
            <b-link to="/major/" class="aat-button btn btn-secondary">
              Assign Major
            </b-link>
          </b-nav>
          <b-nav vertical class="aat-nav-group">
            <b-link to="/cohort_list/" class="nav-link aat-link" title="View all cohorts">
              Cohorts
            </b-link>
            <b-link to="/major_list/" class="nav-link aat-link" title="View all majors">
              Majors
            </b-link>
            <b-link to="/log/" class="nav-link aat-link" title="View all activity">
              Activity Log
            </b-link>
          </b-nav>
          <b-nav vertical class="aat-link-group">
            <b-link href="https://www.tableau.com" class="nav-link aat-link" target="_blank">
              Tableau Selection Tool
            </b-link>
          </b-nav>
        </header>
      </b-col>
      <b-col cols="8" lg="10" class="aat-content-area">
        <b-row>
          <messagearea />
        </b-row>
        <b-row>
          <main class="col">
            <router-view />
          </main>
        </b-row>
      </b-col>
    </b-row>
    <b-row>
      <footer class="aat-footer" role="contentinfo">
        <a href="http://www.uw.edu" class="aat-footer-wordmark">University of Washington</a>
        <div class="aat-footer-links">
          <a href="https://www.washington.edu/online/privacy/">Privacy</a> / <a href="https://www.washington.edu/online/terms/">Terms</a>
        </div>
        <div>© 2019 University of Washington  |  Seattle, WA</div>
      </footer>
    </b-row>
  </b-container>
</template>

<script>
  import MessageArea from "./components/message_area.vue";
  export default {
    name: "LandingPage",
    components: {
      messagearea: MessageArea,
    },
    data(){
      return {
        netid: '',
      };
    },
    mounted() {
      this.netid = window.user_netid;
    },
    methods: {
    }
  };
</script>

<style lang="scss">
  @import '../css/_variables.scss';
  @import '../css/custom.scss';

  // top banner styles
  .aat-app-banner {
    background-color: $banner-bkgnd;
    border-bottom: 1px solid $banner-border;
    font-size: 0.875rem;
    height: 3rem;

    div:first-child {
      border-right: 1px solid $banner-border;
      height: 100%;
      padding: 0.75rem 1rem;
    }
  }

  .aat-logout-link {
    float: right;
    padding: 0.75rem 0;
  }


  // branding styles
  .aat-page-header {
    font-size: 1.5rem;
    font-weight: bold;
    padding: 1.5rem 0;
  }

  .aat-sub-header {
    color: $sub-header;
    font-size: 1rem;
    font-weight: normal;
    text-transform: uppercase;
  }

  .aat-brand-link {
    color: inherit;

    &:hover {
      text-decoration: none;
    }
  }

  .aat-app-info {
    margin-bottom: 1rem;
    text-align: center;
    text-transform: uppercase;

    .aat-app-logo {
      margin: 1rem 0;
      width: 35%;
    }
  }

  .aat-app-name {
    display: block;
    font-size: 1rem;
    line-height: 1.5;

  }

  // side-nav styles
  .aat-main-navbar {
    border-right: 1px solid $uw-light-grey;
    padding: 1rem;
  }

  .aat-nav-group {
    margin: 24px 0 0;

    .aat-link {
      padding: 0.5rem 0 0.5rem 1rem;
    }
  }

  .aat-button {
    margin: 0.5rem;
    padding: 0.5rem 1rem;
  }

  .aat-button.router-link-exact-active {
    background-color: $banner-bkgnd;
    border-color: $banner-border;
    color: $text-color;
    font-weight: bold;

    &:hover {
      background-color: $banner-bkgnd;
      border-color: $banner-border;
      color: inherit;
    }
  }

  .aat-link-group {
    border-top: solid 1px $uw-light-grey;
    margin-top: 1rem;
    padding-top: 0.5rem;

  }

  // main content container styles

  .aat-cohort-manager {
    min-height: 85vh;

    .aat-content-area {
      background-color: $app-bkgnd;
      padding: 0 2rem 2rem;
    }

  }

  // footer styles

  .aat-footer {
    background-color: $uw-purple;
    border-top: 7px solid $uw-light-grey;
    color: $light-text;
    font-size: 0.75rem;
    min-height: 100px;
    min-width: 100%;
    padding: 3rem 3rem 2rem;
    text-align: center;

    .aat-footer-wordmark {
      background: url('/static/cohort_manager/img/uw-sprite.svg') no-repeat 0 -434px transparent;
      display: inline-block;
      overflow: hidden;
      text-indent: -9999px;
      width: 335px;
    }

    .aat-footer-links {
      padding: 0.5rem 0;
    }
  }

  .aat-footer a {
    color: $light-text;

    &:hover {
      color: $uw-metallic;
    }
  }

  // Forms

  .aat-form-section {
    margin: 0 0 3rem;

    .aat-select-inline {
      background: none;
      border-color: $text-color;
      border-radius: 0;
      border-style: none none solid;
      margin: -0.25rem 0.5rem 0;
      padding: 0;
      width: max-content;
    }

  }

  .aat-checkbox {
    margin-top: 2rem;
  }

  //Tables
  .aat-data-table {
    border-bottom: 2px solid $table-border;
    font-size: 0.85rem;
    line-height: 1.3;
  }

  .aat-data-table .aat-data-cell {
    padding: 1rem;

    &.aat-data-nowrap {
      white-space: nowrap;
    }
  }

  .aat-data-split {
    padding-bottom: 0.5rem;
  }

  // Modals

  .aat-modal-container {
    margin: 2rem 1rem 0;
  }

</style>
