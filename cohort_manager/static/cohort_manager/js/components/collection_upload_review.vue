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
        id="app_reassign_checkbox"
        name="app_reassign_checkbox"
        value=""
        class="aat-checkbox"
      >
        Reassign applications that already have a cohort.
      </b-form-checkbox>
      <b-form-checkbox
        id="app_unprotect_checkbox"
        name="app_unprotect_checkbox"
        value=""
        class="aat-checkbox aat-secondary-checkbox"
      >
        Additionally, reassign applications already assigned to <strong>protected cohorts</strong>.
      </b-form-checkbox>
      <b-form-text>
        Note: Applications with a protected cohort will not be reassigned.
      </b-form-text>
    </div>
  </div>
</template>

<script>
  import ApplicationList from "../components/application_list.vue";
  import Vue from "vue/dist/vue.esm.js";
  import VueCookies from "vue-cookies";
  Vue.use(VueCookies);
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
        collection_type: ""
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
    }
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';
  @import '../../css/custom.scss';

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
    margin: 2rem 0 0;

    &.aat-secondary-checkbox {
      margin: 1rem 1.5rem 0;
    }

  }
</style>
