<template>
  <div class="aat-app-add-review">
    <div id="file_name">
      Imported file: {{ uploaded_filename }}
    </div>
    <p id="upload_app_count" class="aat-status-feedback">
      {{ upload_count }} system keys found. <a href="#">Reset</a>
    </p>

    <div role="tablist" class="aat-accordian">
      <b-card no-body class="mb-1">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <b-button v-b-toggle.accordion-assigned block variant="info" href="#">
            Already assigned a {{ collectionType }} (#)
          </b-button>
        </b-card-header>
        <b-collapse id="accordion-assigned" accordion="my-accordion" role="tabpanel">
          <b-card-body>
            <b-card-text><applicationlist application-return="Assigned" :collection-type="collectionType" :applications="already_assigned" /></b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>
      <b-card v-if="collectionType === 'Cohort'" no-body class="mb-1">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <b-button v-b-toggle.accordion-protected block variant="info" href="#">
            Already assigned a protected Cohort (#)
          </b-button>
        </b-card-header>
        <b-collapse id="accordion-protected" accordion="my-accordion" role="tabpanel">
          <b-card-body>
            <b-card-text><applicationlist application-return="Protected" :collection-type="collectionType" /></b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>
      <b-card no-body class="mb-1">
        <b-card-header header-tag="header" class="p-1" role="tab">
          <b-button v-b-toggle.accordion-duplicates block variant="info" href="#">
            Duplicates (#)
          </b-button>
        </b-card-header>
        <span class="aat-accordion-note">Select applications to assign:</span>
        <b-collapse id="accordion-duplicates" visible accordion="my-accordion" role="tabpanel">
          <b-card-body>
            <b-card-text><applicationlist application-return="Duplicate" :collection-type="collectionType" /></b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>
    </div>

    <div id="reassign_app_option">
      <b-form-checkbox
        v-model="is_reassign"
        id="app_reassign_checkbox"
        name="app_reassign_checkbox"
        class="aat-checkbox"
      >
        Reassign applications that already have a cohort.
      </b-form-checkbox>
      <b-form-checkbox
        v-model="is_reassign_protected"
        id="app_unprotect_checkbox"
        name="app_unprotect_checkbox"
        class="aat-checkbox aat-secondary-checkbox"
      >
        Additionally, reassign applications already assigned to <strong>protected cohorts</strong>.
      </b-form-checkbox>
      <b-form-text>
        Note: Applications with a protected cohort will not be reassigned.
      </b-form-text>
    </div>
    <button type="submit" @click="mark_for_submission">
      Submit for processing
    </button>
  </div>
</template>

<script>
  import ApplicationList from "../components/application_list.vue";
  import Vue from "vue/dist/vue.esm.js";
  import VueCookies from "vue-cookies";
  Vue.use(VueCookies);
  const axios = require("axios");
  export default {
    name: "UploadReview",
    components: {
      applicationlist : ApplicationList
    },
    props: {
      uploadResponse: {
        type: Object,
        default: function() {return {};}
      },
      collectionType: {
        type: String,
        default: function() {return [];}
      },
    },
    data(){
      return {
        upload_count: 0,
        collection_id: '',
        uploaded_filename: '',
        text: "This is some text.",
        upload_response: {},
        already_assigned: [],
        already_assigned_protected: [],
        duplicates: [],
        collection_type: "",
        csrfToken: "",
        is_reassign: false,
        is_reassign_protected: false
      };
    },
    watch: {
      upload_response: function(){
        $.each(this.upload_response.assignments, function(idx, assignment){
          if(this.collection_type === "Major"){
            if(assignment.major !== "null"){
              this.already_assigned.push(assignment);
            }
          } else if(this.collection_type === "Cohort") {
            if(assignment.cohort !== "null"){
              this.already_assigned.push(assignment);
            }
          }
        });
      }
    },
    mounted() {
      this.csrfToken = $cookies.get("csrftoken");
      this.collection_type = this.$props.collectionType;
      this.upload_count = this.$props.uploadResponse.assignments.length;
      if(this.$props.collectionType === "Cohort"){
        this.collection_id = this.$props.uploadResponse.assignments[0].cohort;
      }
      else if(this.$props.collectionType === "Major"){
        this.collection_id = this.$props.uploadResponse.assignments[0].major;
      }
      this.uploaded_filename = this.$props.uploadResponse.upload_filename;
      this.upload_response = this.$props.uploadResponse;
    },
    methods: {
      mark_for_submission: function(){
        axios.put(
          '/api/upload/' + this.upload_response.id + "/",
          {'submit': true,
          'is_reassign': this.is_reassign,
          'is_reassign_protected': this.is_reassign_protected},
          {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': this.csrfToken
            }
          }
        ).then(function() {
          this.$router.push({path: '/'});

        });
      },
    },
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';
  @import '../../css/custom.scss';

  // upload issues lists
  .aat-accordian {
    .btn-block {
      text-align: left;
    }

    .aat-accordion-note {
      margin: 1.5rem 1.5rem 0;
    }

    .btn-info {
      background-color: $banner-bkgnd;
      border-style: none;
      color: inherit;
    }
  }

  .aat-checkbox {
    &.aat-secondary-checkbox {
      margin: 1rem 1.5rem 0;
    }

  }
</style>
