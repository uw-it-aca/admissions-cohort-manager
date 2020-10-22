<template>
  <div>
    <collection-upload-file-input
      @fileselected="file_selected"
    />
    <collection-upload-dupe-modal
      v-if="has_dupes"
      :duplicates="dupes"
      collection-type="purplegold"
      @remove-dupes="remove_applications"
    />
    <upload-review
      v-if="has_uploaded"
      :upload-response="upload_response"
      collection-type="purplegold"
      upload-type="file"
    />
  </div>
</template>

<script>
  import CollectionUploadFileInput
    from '../components/collection_upload_file_input';
  import Vuex from "vuex";
  import CollectionUploadDupeModal from "./collection_upload_dupe_modal";
  import UploadReview from "../components/collection_upload_review.vue";


  const axios = require("axios");

  export default {
    name: "PurpleGoldUpload",
    components: {
      CollectionUploadDupeModal,
      CollectionUploadFileInput,
      UploadReview
    },
    data(){
      return {
        file: null,
        csrfToken: null,
        is_uploading: false,
        upload_response: undefined,
        has_dupes: false,
        dupes: undefined,
        has_uploaded: false,
        error_message: undefined,
        invalid_csv: false
      };
    },
    computed: {
      ...Vuex.mapState({
        current_period: state => state.period.current_period,
        cohortOptions: state => state.cohortlist.cohorts
      }),
      assignments: function () {
        if(this.upload_response !== undefined) {
          return this.upload_response.assignments;
        }
        return [];
      },
      ineligibleResidency: function () {
        var ineligible = [];
        $(this.assignments).each(function (idx, value) {
          if(value.is_wa === true || value.is_international === true){
            ineligible.push(value);
          }
        });
        return ineligible;
      },
      alreadyAssigned: function () {
        var assigned = [];
        $(this.assignments).each(function (idx, value) {
          if(value.purple_gold_assigned !== null){
            assigned.push(value);
          }
        });
        return assigned;
      },
      assignedDenied: function() {
        var denied = [],
            vue = this;
        $(this.assignments).each(function (idx, value) {
          if(vue.denied_cohorts.includes(value.assigned_cohort)){
            denied.push(value);
          }
        });
        return denied;
      },
      denied_cohorts: function() {
        var denied_cohorts = [];
        $(this.cohortOptions).each(function (idx, val) {
          if(val.admit_decision === "Deny" || val.admit_decision === "Waitlist"){
            denied_cohorts.push(val.value);
          }
        });
        return denied_cohorts;
      }

    },
    created (){
      this.setCSRF();
      // prefetch cohort list for denied detection
      this.$store.dispatch('cohortlist/get_cohorts', this.current_period);
    },
    mounted() {
    },
    methods: {
      setCSRF() {
        this.csrfToken = $cookies.get("csrftoken");
      },
      file_selected (file) {
        this.file = file;
        this.handleUpload();
      },
      handleUpload() {
        var vue = this;
        let formData = new FormData();
        // Reset error modals
        this.invalid_csv = false;
        this.invalid_manual = false;
        this.is_uploading = true;

        if (this.file !== null){
          this.manual_upload = false;
          formData.append('file', this.file);
        }
        formData.append('comment', this.comment);
        formData.append('qtr_id', this.current_period);
        formData.append('purplegold', true);
        axios.post(
          '/api/upload',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              'X-CSRFToken': this.csrfToken
            }
          }
        ).then(response => {
          vue.is_uploading = false;
          vue.upload_response = response.data;
          var dupes = vue.get_duplicates(this.upload_response.assignments);
          if(dupes.length > 1){
            vue.has_dupes = true;
            vue.dupes = dupes;
          } else{
            vue.has_uploaded = true;
          }
        }).catch(function (err_resp) {
          console.log(err_resp);
          vue.invalid_csv = true;
          try {
            vue.error_message = err_resp.data.error;
          } catch (error) {
            vue.error_message = "Error processing response";
          }
          // vue.handleReset();
        });
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
      remove_applications(list){
        var vue = this,
            request = {'submit': false,
                       'is_reassign': false,
                       'is_reassign_protected': false,
                       'to_delete': list};
        axios.put(
          '/api/upload/' + this.upload_response.id + "/",
          request,
          {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': this.csrfToken
            }
          }
        ).then(function(response) {
          vue.upload_response = response.data;
          vue.has_uploaded = true;
        });
      },
    }
  };
</script>

<style lang="scss">
</style>
