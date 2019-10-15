<template>
  <b-container fluid>
    <b-row class="aat-app-banner">
       <b-navbar toggleable="lg">
        <b-navbar-toggle tabindex="1" target="nav-collapse"></b-navbar-toggle>
          <span class="aat-app-info aat-mobile-brand">
            <a href="/" class="aat-brand-link">
              <img class="aat-app-logo" src="/static/cohort_manager/img/W-Logo-white.png" alt="UW-IT">
              <span class="aat-app-name"><span class="aat-app-name-first">Application</span> Assignment Tool</span>
            </a>
          </span>
          <span class="aat-login-info">
            <span class="aat-lg-only" >Welcome, </span><span id="netid">{{ netid }}</span>
            <a href="#" tabindex="0" class="aat-logout-link">Sign out</a>
          </span>
      </b-navbar>
    </b-row>
    <b-row class="aat-cohort-manager">
      <b-col cols="4" lg="2" class="aat-main-navbar">
        <b-collapse id="nav-collapse" toggleable="lg" class="aat-nav-container">
          <b-navbar-brand class="aat-app-info">
            <a href="/" class="aat-brand-link">
              <img class="aat-app-logo" src="/static/cohort_manager/img/W-Logo.png" alt="UW-IT">
              <span class="aat-app-name"><span class="aat-app-name-first">Application</span> Assignment Tool</span>
            </a>
          </b-navbar-brand>
          <b-navbar class="aat-nav-container">
            <b-navbar-nav class="aat-nav-group aat-assign-group">
              <b-link to="/cohort/" tabindex="1" class="aat-button-override">
                <span aria-hidden="true">+ </span>Assign Cohort
              </b-link>
              <b-link to="/major/" tabindex="1" class="aat-button-override">
                <span aria-hidden="true">+ </span>Assign Major
              </b-link>
            </b-navbar-nav>
            <b-navbar-nav class="aat-nav-group">
              <b-link to="/cohort_list/" tabindex="1" class="nav-link aat-link" title="View all cohorts">
                Cohorts
              </b-link>
              <b-link to="/major_list/" tabindex="1" class="nav-link aat-link" title="View all majors">
                Majors
              </b-link>
              <b-link to="/log/" tabindex="1" class="nav-link aat-link" title="View all activity">
                Activity Log
              </b-link>
            </b-navbar-nav>
            <b-navbar-nav vertical class="aat-link-group">
              <b-link href="https://www.tableau.com" tabindex="1" class="nav-link aat-link" target="_blank">
                Tableau Selection Tool
              </b-link>
            </b-navbar-nav>
          </b-navbar>
        </b-collapse>
      </b-col>
      <b-col cols="12" lg="10" class="aat-content-area">
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

  
  // hide for small screens
  @media screen and (max-width: 992px) {
    .aat-lg-only {
      display: none;
    }
  }

  // top banner styles
  .aat-app-banner {
    background-color: $uw-purple;
    border-bottom: 1px solid $banner-border;
    color: #fff;
    font-size: 0.75rem;

    a {
      color: #fff;
    }

    a:hover,
    a:focus {
      color: $uw-light-grey;
    }

    nav {
      flex: auto;
    }

    div:first-child {
      border-right: 1px solid $banner-border;
      height: 100%;
      padding: 0.75rem 1rem;
    }

    .aat-banner-content {
      flex: auto;
    }
  }

  .aat-logout-link {
    float: right;
    padding-left: 2rem;
  }

  @media screen and (min-width: 992px) {    
    .aat-login-info {
      flex: auto;
      font-weight: 100;
    }
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
    line-height: 1.25;

    &:hover,
    &:focus {
      text-decoration: none;
    }
  }

  .aat-app-info {
    display: none !important;
    margin: 0 auto !important;
    text-align: center;
    text-transform: uppercase;
    width: 160px;

    &.aat-mobile-brand {
      display: block !important;
    }

    .aat-app-logo {
      float: left;
      margin: 0.25rem 0;
      min-width: 40px;
      width: 15%;
    }
  }

  .aat-app-name {
    color: #fff;
    display: block;
    font-size: 0.7rem;
    font-weight: 700;
    padding-left: 0.25rem;

    .aat-app-name-first {
      display: block;
      font-size: 1rem;
      font-weight: 800;
    }
  }

  @media screen and (min-width: 992px) {
    .aat-app-info {
      display: block !important;
      margin: 1rem auto !important;

      &.aat-mobile-brand {
        display: none !important;

      }

      .aat-app-name {
        color: $uw-purple;
      }
    }
  }

  // side-nav styles
  .aat-nav-container {
    align-items: start !important;
    clear: both;
    flex-direction: column !important;
  }
  
  .aat-main-navbar {
    border-right: 1px solid $uw-light-grey;
    max-width: 220px !important;
    padding: 0 !important;
    position: absolute !important;
    z-index: 99;
  }

  .aat-nav-group {
    flex-direction: column !important;
    margin: 24px 0 0;

    &.aat-assign-group {
      margin-top: 0;
      width: 100%;
    }

    .aat-link {
      padding: 0.5rem 0 0.5rem 1rem;
    }
  }

  .aat-button-override {
    background: none;
    border-color: $uw-light-grey;
    border-radius: 0;
    border-style: none none solid;
    border-width: 1px;
    color: $nav-text;
    margin: 0 -1rem;
    padding: 1rem 0 1rem 1.5rem;
    text-align: left;

    &:hover,
    &:focus {
      background-color: $grey-bkgnd;
      border-color: $banner-border;
      color: inherit;
    }
  }

  .aat-button-override.router-link-exact-active {
    color: $text-color;
    font-weight: bold;
  }

  .aat-link-group {
    border-top: solid 1px $uw-light-grey;
    margin-top: 1rem;
    padding-top: 0.5rem;

  }

  @media screen and (min-width: 992px) {
    .aat-main-navbar {
      max-width: none !important;
      position: relative !important;
    }

    .aat-nav-container {
      display: block !important;
    }
  }


  // main content container styles

  .aat-cohort-manager {
    min-height: 85vh;
    overflow: hidden;

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
      margin-bottom: 1rem;
      overflow: hidden;
      text-indent: -9999px;
      width: 335px;
    }

    .aat-footer-links {
      font-size: 0.8725rem;
      padding: 0.5rem 0;
    }
  }

  .aat-footer a {
    color: $light-text;

    &:hover,
    &:focus {
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
