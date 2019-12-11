<template>
  <div class="aat-app-add-review">
    <div id="upload_app_count">
      <span v-if="uploadType === 'file'"><i class="fas fa-file-csv" /><span class="sr-only">Uploaded file: </span>{{ uploaded_filename }} </span><span v-else><i class="fas fa-file-alt" /><span class="sr-only">Applications manually added </span></span><a href="#" class="aat-reset-link" @click.prevent="reset_upload">Reset</a>
    </div>
    <p id="file_name" class="aat-status-feedback">
      {{ upload_count }} applications found.
    </p>
    <div v-if="reassign_any" id="app_reassign_accordion" role="tablist" class="aat-accordian">
      <b-card no-body class="mb-1">
        <b-card-header v-if="has_assigned" header-tag="header" class="p-1" role="tab">
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
      <b-card v-if="has_protected" no-body class="mb-1">
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
      <div id="reassign_collection" class="aat-reassign-checkbox">
        <b-form-checkbox
          id="app_reassign_checkbox"
          v-model="is_reassign"
          name="app_reassign_checkbox"
          value=""
          class="aat-checkbox"
        >
          Reassign applications that already have a {{ collectionType }}.
        </b-form-checkbox>
        <span v-if="uploadType === 'file'">
          <b-form-text v-if="collectionType === 'Cohort'">
            Note: Applications with a protected cohort will not be reassigned.
          </b-form-text>
        </span>
        <span v-else-if="reassign_any" id="reassign_collection_protected">
          <b-form-checkbox
            id="app_unprotect_checkbox"
            v-model="is_reassign_protected"
            name="app_unprotect_checkbox"
            value=""
            class="aat-checkbox aat-secondary-checkbox"
          >
            Additionally, reassign applications already assigned to <strong>protected cohorts</strong>.
          </b-form-checkbox>
        </span>
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
        default: function() {return [];}
      },
      uploadType: {
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
      }
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
        this.duplicates = this.get_duplicates(this.upload_response.assignments);
      },
      is_reassign: function(value){
        if(typeof value === "string"){
          this.$emit("is_reassign", true);
        } else {
          this.$emit("is_reassign", false);
        }
      },
      is_reassign_protected: function(value){
        if(typeof value === "string"){
          this.$emit("is_reassign_protected", true);
        } else {
          this.$emit("is_reassign_protected", false);
        }
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
      proc: function(list){
        this.$emit("dupeToRemove", list);
      },
      reset_upload: function(){
        this.$emit('upload_reset');
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
      }
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
  .aat-accordian {
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

  .aat-checkbox {
    &.aat-secondary-checkbox {
      margin: 1rem 1.5rem 0;
    }
  }

  .aat-reassign-checkbox {
    margin-left: 0.5rem;
  }

  .aat-reset-link {
    margin-left: 0.5rem;
  }
</style>
