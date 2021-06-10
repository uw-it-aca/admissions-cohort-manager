<template>
  <div class="aat-app-add-review aat-form-section">
    <div id="upload_app_count">
      <span v-if="uploadType === 'file'">
        <i class="fas fa-file-csv" />
        <span class="sr-only">Uploaded file: </span>
        {{ uploaded_filename }}
        <a href="#" class="aat-reset-link" @click.prevent="reset_upload">Reset</a>
      </span>
      <span v-else>
        <span class="sr-only">Applications manually added </span>
      </span>
    </div>
    <p id="file_name" class="aat-status-feedback">
      <span class="aat-application-count">{{ upload_count }} {{ 'application' | pluralize(upload_count) }} found.
        <span v-if="uploadType === 'list'">
          <a href="#" class="aat-reset-link" @click.prevent="reset_upload">Clear applications</a>
        </span>
      </span>
    </p><div v-if="no_cohort_count > 0" class="no-cohort-count-alert">
      <b-icon-exclamation-triangle /> <span class="no-cohort-count-text">{{ no_cohort_count }} of these applications do not have a cohort assignment.</span>
    </div>
    <div v-if="reassign_any" id="app_reassign_accordion" class="aat-collapse">
      <b-card v-if="already_assigned.length < 100" no-body class="mb-1">
        <b-card-header v-if="has_assigned" header-tag="header" class="p-1">
          <b-button v-b-toggle.collapse-assigned block variant="info" href="#">
            Already have a <span v-if="collectionType === 'Cohort'">cohort</span><span v-else>major</span> ({{ already_assigned.length }})
          </b-button>
        </b-card-header>
        <b-collapse id="collapse-assigned">
          <b-card-body>
            <b-card-text><applicationlist application-return="Assigned" :collection-type="collectionType" :applications="already_assigned" /></b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>
      <div v-else-if="already_assigned.length > 0" class="aat-assigned-count">
        {{ already_assigned.length }} are already assigned to a <span v-if="collectionType === 'Cohort'">cohort</span><span v-else>major</span>.
      </div>
      <b-card v-if="has_protected && already_assigned_protected.length < 100" no-body class="mb-1">
        <b-card-header header-tag="header" class="p-1">
          <b-button v-b-toggle.collapse-protected block variant="info" href="#">
            Already have a protected cohort ({{ already_assigned_protected.length }})
          </b-button>
        </b-card-header>
        <b-collapse id="collapse-protected">
          <b-card-body>
            <b-card-text><applicationlist application-return="Protected" :collection-type="collectionType" :applications="already_assigned_protected" /></b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>
      <div v-else-if="already_assigned_protected.length > 0" class="aat-assigned-count">
        {{ already_assigned_protected.length }} are already assigned to protected cohorts.
      </div>
      <div v-if="collectionType === 'Cohort'" id="reassign_collection" class="aat-reassign-checkbox">
        <b-form-checkbox
          v-if="has_assigned"
          id="app_reassign_checkbox"
          v-model="is_reassign"
          name="app_reassign_checkbox"
          value=""
          class="aat-checkbox"
        >
          Reassign applications that already have a non-protected cohort.
        </b-form-checkbox>
        <span v-if="uploadType === 'file'">
          <b-form-text>
            Note: Applications with a protected cohort will not be reassigned.
          </b-form-text>
        </span>
        <span v-else-if="has_protected && uploadType !== 'bulk'" id="reassign_collection_protected">
          <b-form-checkbox
            id="app_unprotect_checkbox"
            v-model="is_reassign_protected"
            name="app_unprotect_checkbox"
            value=""
            class="aat-checkbox"
          >
            Reassign applications that already have a protected cohort.
          </b-form-checkbox>
        </span>
      </div>
      <div v-else>
        <b-form-text class="aat-assigned-count">
          Note: These applications will be reassigned to new major.
        </b-form-text>
      </div>
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
        default: function() {return "";}
      },
      uploadType: {
        type: String,
        default: function() {return "";}
      },
      collectionOptions: {
        type: Array,
        default: function () {return[];}
      },
      collectionId: {
        type: String,
        default: function () {return "";}
      },
    },
    data(){
      return {
        uploaded_filename: '',
        text: "This is some text.",
        already_assigned: [],
        already_assigned_protected: [],
        duplicates: [],
        collection_type: "",
        csrfToken: "",
        is_reassign: false,
        is_reassign_protected: false,
      };
    },
    computed: {
      has_assigned : function() {
        return this.already_assigned.length > 0;
      },
      has_protected: function() {
        var has_protected = this.already_assigned_protected.length > 0,
            is_cohort = this.collectionType === "Cohort";
        return has_protected && is_cohort;
      },
      reassign_any: function(){
        return this.has_assigned || this.has_protected;
      },
      protected_cohort_ids: function(){
        var protected_ids = [];
        $.each(this.collectionOptions, function(idx, cohort){
          if(cohort.protected){
            protected_ids.push(cohort.value);
          }
        });
        return protected_ids;
      },
      upload_count: function(){
        var valid_count = 0,
            assignments = this.$props.uploadResponse.assignments;
        for(var assign in assignments){
          if(!assignments[assign].application_not_found){
            valid_count += 1;
          }
        }
        return valid_count;
      },
      no_cohort_count: function(){
        var no_cohort_count = 0;
        $.each(this.uploadResponse.assignments, function(idx, assignment){
          if(assignment.assigned_cohort === null){
            no_cohort_count++;
          }
        });
        return no_cohort_count;
      }
    },
    watch: {
      uploadResponse: function(){
        var vue = this;
        this.already_assigned = [];
        this.already_assigned_protected = [];
        $.each(this.uploadResponse.assignments, function(idx, assignment){
          if(vue.collectionType === "Major"){
            if(assignment.assigned_major !== null){
              $.each(vue.collectionOptions, function (idx, collection) {
                if(collection.value === assignment.assigned_major){
                  assignment.description = collection.text;
                }
                assignment.protected = false;
              });
              vue.already_assigned.push(assignment);
            }
          } else if(vue.collectionType === "Cohort") {
            if(assignment.assigned_cohort !== null && String(assignment.assigned_cohort) !== vue.collectionId){
              if(vue.protected_cohort_ids.includes(assignment.assigned_cohort)){
                vue.already_assigned_protected.push(assignment);
              } else {
                if(assignment.assigned_cohort !== 0){
                  vue.already_assigned.push(assignment);
                }
              }
              $.each(vue.collectionOptions, function (idx, collection) {
                if(collection.value === assignment.assigned_cohort){
                  assignment.description = collection.description;
                  assignment.protected = collection.protected;
                }
              });
            }
          }
        });
        this.duplicates = this.get_duplicates(this.uploadResponse.assignments);
      },
      is_reassign: function(value){
        if(typeof value === "string"){
          this.$emit("is-reassign", true);
        } else {
          this.$emit("is-reassign", false);
        }
      },
      is_reassign_protected: function(value){
        if(typeof value === "string"){
          this.$emit("is-reassign-protected", true);
        } else {
          this.$emit("is-reassign-protected", false);
        }
      }
    },
    mounted() {
      this.csrfToken = $cookies.get("csrftoken");
      this.collection_type = this.$props.collectionType;
      this.uploaded_filename = this.$props.uploadResponse.upload_filename;
    },
    methods: {
      proc: function(list){
        this.$emit("dupe-to-remove", list);
      },
      reset_upload: function(){
        this.$emit('upload-reset');
      },
      get_duplicates: function(assignments){
        var syskeys = {},
            dupe_assignments =[];
        $.each(assignments, function(idx, assignment){
          if(assignment.system_key in syskeys){
            syskeys[assignment.system_key] += 1;
          } else {
            syskeys[assignment.system_key] = 1;
          }
        });
        $.each(assignments, function(idx, assignment) {
          if(syskeys[assignment.system_key] > 1){
            dupe_assignments.push(assignment);
          }
        });
        return dupe_assignments;
      },
    },
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';

  //upload icon
  .fa-file-csv,
  .fa-file-alt {
    font-size: 1.375rem;
    width: 1.5rem;
  }

  // upload issues lists
  .aat-collapse {
    .btn-block {
      text-align: left;
    }

    .btn-block.btn-info,
    .btn-block.btn-info:active {
      background-color: transparent;
      border-style: none;
      color: $link-blue;
    }
  }

  .aat-reassign-checkbox {
    margin-left: 0.5rem;

    .aat-checkbox {
      margin-top: 1rem;
    }
  }

  .aat-reset-link {
    font-weight: normal;
    margin-left: 0.5rem;
  }
</style>
