<template>
  <b-container fluid>
    <b-row class="aat-app-banner">
      <h2 id="aat_navbar_header" class="sr-only">
        Main Navigation
      </h2>
      <b-navbar aria-labelledby="aat_navbar_header" toggleable="lg">
        <b-navbar-toggle tabindex="1" target="nav-collapse" />
        <span class="aat-app-info aat-mobile-brand">
          <a href="/" class="aat-brand-link">
            <img class="aat-app-logo" src="/static/cohort_manager/img/AAT-Logo-white.svg" alt="UW-IT">
            <span class="sr-only">Application Assignment Tool</span>
          </a>
        </span>
        <span class="aat-login-info">
          <h3 id="aat_login_header" class="sr-only">Your information</h3>
          <span aria-labelledby="aat_login_header" class="aat-lg-only">Welcome, </span><span id="netid">{{ netid }}</span>
          <a href="/saml/logout" tabindex="0" class="aat-logout-link">Sign out</a>
        </span>
      </b-navbar>
    </b-row>
    <b-row class="aat-cohort-manager">
      <b-collapse id="nav-collapse" toggleable="lg" class="aat-nav-container aat-main-navbar col-lg-2 col-12">
        <b-navbar-brand class="aat-app-info">
          <a href="/" tabindex="1" class="aat-brand-link">
            <img class="aat-app-logo" src="/static/cohort_manager/img/AAT-Logo-purple.svg" alt="UW-IT">
            <span class="sr-only">Application Assignment Tool</span>
          </a>
        </b-navbar-brand>
        <b-navbar class="aat-nav-container">
          <h3 id="aat_collection_assignment_header" class="sr-only">
            Assign Applications
          </h3>
          <b-navbar-nav aria-labelledby="aat_collection_assignment_header" class="aat-nav-group aat-assign-group">
            <li class="aat-button-override">
              <b-link to="/cohort/" tabindex="1">
                Assign Cohort
              </b-link>
            </li>
            <li class="aat-button-override">
              <b-link to="/major/" tabindex="1">
                Assign Major
              </b-link>
            </li>
          </b-navbar-nav>
          <h3 id="aat_navlink_header" class="sr-only">
            Go to:
          </h3>
          <b-navbar-nav aria-labelledby="aat_navlink_header" class="aat-nav-group">
            <li>
              <b-link to="/cohort_list/" tabindex="1" class="nav-link aat-link" title="View all cohorts">
                Cohorts
              </b-link>
            </li>
            <li>
              <b-link to="/major_list/" tabindex="1" class="nav-link aat-link" title="View all majors">
                Majors
              </b-link>
            </li>
            <li>
              <b-link to="/log/" tabindex="1" class="nav-link aat-link" title="View all activity">
                Activity Log
              </b-link>
            </li>
          </b-navbar-nav>
          <h3 id="aat_external_link_header" class="sr-only">
            Other Tools
          </h3>
          <b-navbar-nav aria-labelledby="aat_external_link_header" vertical class="aat-nav-group">
            <li>
              <b-link href="https://bitools.uw.edu/#/site/Transitional/workbooks/6500/views" tabindex="1" class="nav-link aat-link aat-external-link" target="_blank">
                Tableau Selection Tool
              </b-link>
              <b-link href="https://crm.recruit.uw.edu/Seattle" tabindex="1" class="nav-link aat-link" target="_blank">
                CRM Recruit
              </b-link>
            </li>
          </b-navbar-nav>
        </b-navbar>
      </b-collapse>
      <b-col cols="12" lg="10" class="aat-content-area">
        <b-row>
          <messagearea
            :message-string="message"
            :alertType="alertType"
          />
        </b-row>
        <b-row class="aat-adperiod-container" v-if="show_period_picker">
          <label class="sr-only" for="aat_adperiod_select">Select Admission Period</label>
          <b-form-select id="aat_adperiod_select"
                         v-model="current_admission_period"
                         class="aat-adperiod-select"
                         :class="{disabled: admission_periods.length < 2}"
                         :options="admission_periods"
                         @change="set_default_period"
          />
        </b-row>
        <b-row class="aat-main-content-container">
          <main ref="main" aria-labelledby="aat_page_header" class="col aat-main-container">
            <router-view
              v-if="period_set"
              :cur_period="cur_period"
              :periods="admission_periods"
              @showMessage="show_message"
            />
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
        <div class="aat-footer-copyright">© 2020 University of Washington  |  Seattle, WA</div>
      </footer>
    </b-row>
  </b-container>
</template>

<script>
  import MessageArea from "./components/message_area.vue";
  import { EventBus } from "./main";

  const axios = require("axios");
  export default {
    name: "FullBase",
    components: {
      messagearea: MessageArea,
    },
    data(){
      return {
        current_admission_period: '',
        admission_periods: [],
        disable_period_select: false,
        netid: '',
        message: '',
        navCount: 0,
        cur_period: null,
        alertType: null,
        show_period_picker: true
      };
    },
    computed: {
      period_set: function () {
        return this.cur_period !== null;
      }
    },
    watch: {
      $route(){
        this.set_period_picker_visibility();
        //Set focus for accessibility purposes
        this.$refs.main.focus();
        // Hide the message on the next route AFTER the post-upload one
        if(this.message.length > 0){
          this.navCount++;
          if (this.navCount > 1){
            this.message = '';
            this.navCount = 0;
          }
        }
      },
      current_admission_period: function(period){
        this.cur_period = period;
        EventBus.$emit('period_change', period);
      }
    },
    mounted() {
      this.netid = window.user_netid;
      this.get_periods();
      this.set_period_picker_visibility();
    },
    methods: {
      set_period_picker_visibility() {
        if(this.$router.currentRoute.path === "/log/"){
          this.show_period_picker = false;
        } else {
          this.show_period_picker = true;
        }
      },
      show_message(msg, type) {
        var vue = this;
        this.message = msg;
        this.alertType = type;
        // Hides the message after 10 seconds
        window.setTimeout(function () {
          vue.message = '';
        }, 10000);
      },
      get_periods() {
        var vue = this;
        axios.get(
          '/api/periods/',
        ).then(response => {
          vue.admission_periods = response.data;

          var saved_period = this.get_saved_period();
          if(saved_period === null){
            $.each(response.data, function (idx, period) {
              if(period.current === true){
                vue.current_admission_period = period.value;
                vue.set_default_period(period.value);
              }
            });
          } else {
            vue.current_admission_period = saved_period;
          }

        });
      },
      set_default_period(period) {
        $cookies.set('default_period', period, "1y");
      },
      get_saved_period() {
        return $cookies.get('default_period');
      }
    }
  };
</script>

<style lang="scss">
  // import base.scss which inherits the custom theme
  @import '../css/base.scss';
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
      color: $uw-metallic;
    }
    nav {
      flex: auto;
      padding: 1rem;
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
    display: block;
  }
  @media screen and (min-width: 992px) {
    .aat-login-info {
      flex: auto;
      font-weight: 600;
    }
    .aat-logout-link {
      float: right;
      margin-left: 2rem;
    }
  }
  // branding styles
  .aat-page-header {
    font-size: 2rem;
    padding: 1.5rem 0;
  }
  .aat-sub-header {
    color: $text-color;
    font-size: 1.75rem;
    font-weight: 600;
    h3 {
      font-size: 1.5rem;
    }
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
    max-width: 160px;
    text-align: center;
    text-transform: uppercase;
    &.aat-mobile-brand {
      display: block !important;
    }
    &.aat-mobile-brand .aat-app-logo {
      margin: 0.25rem 0;
      min-width: unset;
    }
    .aat-app-logo {
      min-width: 120px;
      width: 100%;
    }
  }
  @media screen and (min-width: 992px) {
    .aat-app-info {
      display: block !important;
      margin: 1rem auto !important;
      &.aat-mobile-brand {
        display: none !important;
      }
    }
  }
  // admission period select
  .aat-content-area {
    .aat-adperiod-select {
      float: right;
      font-size: 0.75rem;
      margin: 1rem 0;
      width: auto;
    }
  }
  // side-nav styles
  .aat-nav-container {
    align-items: start !important;
    clear: both;
    flex-direction: column !important;
    padding: 0;
  }
  .aat-main-navbar {
    border-bottom: 2px solid $uw-light-grey;
    max-width: 100% !important;
    position: relative !important;
    width: 100%;
  }
  .aat-nav-group {
    flex-direction: column !important;
    margin: 0.5rem 0 0;
    width: 100%;
    &.aat-assign-group {
      border-top: solid 1px $uw-light-grey;
      margin-top: 0;
      width: 100%;
    }
  }
  @media (min-height: 500px) and (min-width: 992px) {
    .aat-nav-container {
      background-color: #fff;
      overflow-x: hidden;
      position: fixed;
      width: 16.56%;
    }
  }
  .aat-link {
    padding: 0.5rem 1rem !important;
  }
  .aat-button-override {
    background: none;
    border-color: $uw-light-grey;
    border-radius: 0;
    border-style: none none solid;
    border-width: 1px;
    color: $text-color;
    margin: 0 -1rem;
    text-align: left;
    a:hover {
      background-color: $nav-hover-bkgnd;
      color: $text-black;
      text-decoration: none;
    }
    a:focus {
      background-color: $nav-hover-bkgnd;
      color: $text-black;
      text-decoration: none;
    }
  }
  .aat-button-override .router-link-exact-active {
    background-color: $nav-active-bkgnd;
    color: $light-text;
  }
  .aat-button-override a {
    color: $text-color;
    display: block;
    padding: 1rem 0 1rem 2rem;
    width: 100%;
    &::after {
      border-style: solid;
      border-width: 0 2px 2px 0;
      content: '';
      margin-top: 0.6rem;
      padding: 2px;
      position: absolute;
      right: 1.5rem;
      transform: rotate(-45deg);
    }
  }
  .aat-external-link {
    border-top: solid 1px $uw-light-grey;
    padding-top: 1rem !important;
  }
  @media screen and (min-width: 992px) {
    .aat-main-navbar {
      border-bottom-style: none;
      max-width: none !important;
      position: relative !important;
      width: auto;
    }
    .aat-nav-container {
      display: block !important;
    }
    .aat-main-navbar {
      border-right: 1px solid $uw-light-grey;
      padding: 0 !important;
      position: relative !important;
    }
  }
  // main content container styles
  html {
    background-color: $uw-purple;
  }
  .aat-cohort-manager {
    min-height: 70vh;
    overflow: hidden;
    .aat-content-area {
      background-color: $app-bkgnd;
    }
  }
  .aat-main-container {
    padding-bottom: 3rem;
    padding-left: 1.5rem;
  }
  .aat-adperiod-container {
    position: absolute;
    right: 2rem;
    z-index: 99;
  }
  // footer styles
  .aat-footer {
    background-color: $uw-purple;
    border-top: 7px solid $uw-light-grey;
    color: $light-text;
    font-size: 0.75rem;
    min-height: 100px;
    min-width: 100%;
    text-align: center;
    .aat-footer-wordmark {
      background: url('/static/cohort_manager/img/uw-sprite.svg') no-repeat 0 -434px transparent;
      display: inline-block;
      height: 22px;
      margin-bottom: 1rem;
      margin-top: 3rem;
      overflow: hidden;
      text-indent: -9999px;
      width: 335px;
    }
    .aat-footer-copyright {
      margin-bottom: 1rem;
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
      border-color: $banner-border;
      width: max-content;
    }
  }
  .aat-checkbox {
    margin-top: 2rem;
  }
  //Tables
  .aat-data-table {
    border-bottom: 2px solid $table-border;
    font-size: 0.875rem;
    line-height: 1.3;
    .aat-table-header.aat-data-cell {
      color: $sub-header;
      font-size: 0.75rem !important;
    }
    .aat-data-cell.center {
      text-align: center;
    }
  }
  .aat-data-table .aat-data-cell {
    vertical-align: baseline;
    &.aat-data-nowrap {
      white-space: nowrap;
    }
  }
  .aat-data-split {
    padding-bottom: 0.5rem;
  }
  .table-hover tbody tr:focus-within {
    background-color: rgba(0, 0, 0, 0.075);
    color: #212529;
  }
  .row .aat-actions-cell {
    opacity: 0;
  }
  .aat-actions-cell:focus-within {
    opacity: 1;
  }
  tbody tr:hover .aat-actions-cell {
    opacity: 1;
  }
  .b-table[aria-busy='true'] .b-table-busy-slot .text-info {
    padding: 3rem 0;
  }
  @media screen and (max-width: 650px) {
    .row .aat-actions-cell {
      opacity: 1;
    }
  }
  // Modals
  .modal-body {
    margin: 2rem 0.5rem;
  }
  .aat-processing-message {
    margin: 2rem 1rem;
  }
  .aat-modal {
    border: 4px solid $uw-purple;
    box-shadow: 2px 3px 5px #777;
    .modal-title {
      color: $uw-purple;
    }
  }
  .aat-modal-box {
    background-color: rgba(255, 255, 255, 0.5);
  }
  // Collapse
  .card-header {
    background: $light-grey-bkgnd;
    a::after {
      border-style: solid;
      border-width: 0 2px 2px 0;
      content: '';
      display: inline-block;
      padding: 2px;
      transform: rotate(-45deg);
      transition: transform 0.5s;
      vertical-align: middle;
    }
    a:not(.collapsed)::after {
      transform: rotate(45deg);
    }
    .btn-block.collapsed::after {
      transform: rotate(-45deg) !important;
    }
  }
  // Spinner
  .spinner-border,
  .b-table-busy-slot .text-info,
  .aat-processing-text {
    color: $uw-purple !important;
  }
</style>