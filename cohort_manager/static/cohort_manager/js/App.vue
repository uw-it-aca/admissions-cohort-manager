<template>
  <b-container fluid>
    <b-row class="aat-app-banner">
      <b-col cols="4" lg="2" >
      Welcome, <span id="netid">{{ netid }}</span>
      </b-col>
      <b-col cols="8" lg="10"> 
        <a href="#" class="aat-logout-link">Sign out</a>
      </b-col>
    </b-row>
    <b-row class="aat-cohort-manager">
      <b-col cols="4" lg="2" class="aat-main-navbar">
        <header>
          <div class="aat-app-info">
            <a href="/" class="aat-brand-link">
              <img class="aat-app-logo" src="/static/cohort_manager/img/W-Logo.png" alt="UW-IT"/>
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
            <b-link to="/cohort_list/" class="nav-link aat-link">
              Cohorts
            </b-link>
            <b-link to="/major_list/" class="nav-link aat-link">
              Majors
            </b-link>
            <b-link to="/log/" class="nav-link aat-link">
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
          <main>
            <router-view />
          </main>
        </b-row>
      </b-col>
    </b-row>
    <b-row >
      <footer class="aat-footer">
        <a href="http://www.uw.edu" class="aat-footer-wordmark">University of Washington</a>
        <div class="aat-footer-links"><a href="https://www.washington.edu/online/privacy/">Privacy</a> / <a href="https://www.washington.edu/online/terms/">Terms</a></div>
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

  .aat-page-header {
    font-size: 1.5rem;
    font-weight: bold;
    padding: 1.5rem 0;
  }

  .aat-app-banner {
    background-color: #aaa;
    border-bottom: 1px solid #999;
    font-size: 0.875rem;
    height: 3rem;
    
    div:first-child {
      border-right: 1px solid #999;
      height: 100%;
      padding: 0.75rem 1rem;

    }

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

  .aat-app-name {
    display: block;
    font-size: 1rem;
    line-height: 1.5;

  }

  .aat-main-navbar {
    border-right: 1px solid #999;
    height: 100%;
    padding: 1rem;
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
    background-color: #cdcdcd;
    border-color: #aaa;
    color: #444;
    font-weight: bold;

    &:hover {
      background-color: #cdcdcd;
      border-color: #aaa;
      color: inherit;
    }
  }

  .aat-link-group {
    border-top: solid 1px #666;
    margin-top: 1rem;
    padding-top: 0.5rem;

  }

  .aat-logout-link {
    float: right;
    padding: 0.75rem 0;
  }

  .aat-cohort-manager {
    height: 100vh;

    .aat-content-area {
      background-color: #fff;
      padding: 0 3rem 3rem;
    }

  }

  .aat-footer {
    background-color: #4b2e83;
    border-top: 7px solid #999;
    color: #fff;
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
    color: #fff;
    
    &:hover {
      color: #e8e3d3;
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

  //Tables
  .aat-data-table {
    border-bottom: 2px solid rgba(0, 0, 0, 0.05);
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
