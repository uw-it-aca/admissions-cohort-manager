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
    <div v-if="has_issues" class="aat-collapse">
      <!--      Functionality disabled until we switch to doing lookups-->
      <b-card v-if="invalid_residency.length < 100" no-body class="mb-1">
        <b-card-header v-if="invalid_residency" header-tag="header" class="p-1">
          <b-button v-b-toggle.collapse-resident block variant="info" href="#">
            Wa Resident / International ({{ invalid_residency.length }})
          </b-button>
        </b-card-header>
        <b-collapse id="collapse-resident">
          <b-card-body>
            <b-card-text>
              <application-list
                application-return="Assigned"
                collection-type="purplegold"
                :applications="invalid_residency"
              />
            </b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>

      <b-card v-if="already_assigned.length < 100" no-body class="mb-1">
        <b-card-header v-if="already_assigned" header-tag="header" class="p-1">
          <b-button v-b-toggle.collapse-assigned block variant="info" href="#">
            Already assigned an award ({{ already_assigned.length }})
          </b-button>
        </b-card-header>
        <b-collapse id="collapse-assigned">
          <b-card-body>
            <b-card-text>
              <application-list
                application-return="Assigned"
                collection-type="purplegold"
                :applications="already_assigned"
              />
            </b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>

      <b-card v-if="denied_cohort.length < 100" no-body class="mb-1">
        <b-card-header v-if="denied_cohort" header-tag="header" class="p-1">
          <b-button v-b-toggle.collapse-deny block variant="info" href="#">
            Assigned to "Deny" or "Waitlist" cohort ({{ denied_cohort.length }})
          </b-button>
        </b-card-header>
        <b-collapse id="collapse-deny">
          <b-card-body>
            <b-card-text>
              <application-list
                application-return="Assigned"
                collection-type="purplegold"
                :applications="denied_cohort"
              />
            </b-card-text>
          </b-card-body>
        </b-collapse>
      </b-card>-->
    </div>
    <collection-comment
      @comment="update_comment"
    />
    <b-button type="submit" variant="primary" :disabled="!has_uploaded" @click="mark_for_submission">
      Submit
    </b-button>
    <collection-submit-modal
      :show-submitting="show_submitting_modal"
      :show-timeout="show_timeout_modal"
    />
  </div>
</template>

<script>
  import CollectionUploadFileInput
    from '../components/collection_upload_file_input';
  import Vuex from "vuex";
  import CollectionUploadDupeModal from "./collection_upload_dupe_modal";
  import UploadReview from "../components/collection_upload_review.vue";
  import ApplicationList from "../components/application_list";
  import CollectionComment from "../components/collection_comment";
  import CollectionSubmitModal from "../components/collection_submit_modal";


  const axios = require("axios");

  export default {
    name: "PurpleGoldUpload",
    components: {
      CollectionUploadDupeModal,
      CollectionUploadFileInput,
      UploadReview,
      ApplicationList,
      CollectionComment,
      CollectionSubmitModal
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
        invalid_csv: false,
        denied_cohort: [],
        invalid_residency: [],
        already_assigned: [],
        has_issues: false,
        applications: [],
        comment: "",
        is_submitting: false,
        show_submitting_modal: false,
        show_timeout_modal: false
      };
    },
    computed: {
      ...Vuex.mapState({
        current_period: state => state.period.current_period,
        cohortOptions: state => state.cohortlist.cohorts
      }),
      deniedCohorts: function() {
        var denied_cohorts = [];
        $(this.cohortOptions).each(function (idx, val) {
          if(val.admit_decision === "Deny" || val.admit_decision === "Waitlist"){
            denied_cohorts.push(val.value);
          }
        });
        return denied_cohorts;
      }
    },
    watch: {
      applications: function () {
        // Disabled till we get data
        // this.get_invalid();
      }
    },
    created (){
      this.setCSRF();
      // prefetch cohort list for denied detection
      this.$store.dispatch('cohortlist/get_cohorts', this.current_period);
    },
    methods: {
      update_comment(comment){
        this.comment = comment;
      },
      get_invalid() {
        var denied = [],
            assigned = [],
            ineligible = [],
            vue = this;
        this.has_issues = false;
        $(this.applications).each(function (idx, value) {
          if(vue.deniedCohorts.includes(value.assigned_cohort)){
            denied.push(value);
          }
          if(value.is_wa === true || value.is_international === true){
            ineligible.push(value);
          }
          if(value.purple_gold_assigned !== null){
            assigned.push(value);
          }
        });
        if (denied.length > 0 || assigned.length > 0 || ineligible.length > 0){
          this.has_issues = true;
        }
        this.denied_cohort = denied;
        this.already_assigned = assigned;
        this.invalid_residency = ineligible;

      },
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
          vue.applications = this.upload_response.assignments;
          vue.has_uploaded = true;
          // Functionality disabled until we switch to doing lookups
          // var dupes = vue.get_duplicates(vue.applications);
          // if(dupes.length > 1){
          //   vue.has_dupes = true;
          //   vue.dupes = dupes;
          // } else{
          //   vue.has_uploaded = true;
          // }
        }).catch(function (err_resp) {
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
          vue.applications = vue.upload_response.assignments;
          vue.has_uploaded = true;
        });
      },
      mark_for_submission(){
        var vue = this,
            request = {'is_submitted': true,
                       'is_reassign': this.is_reassign,
                       'is_reassign_protected': this.is_reassign_protected,
                       'to_delete': this.to_remove,
                       'comment': this.comment,
                       'purplegold': true};
        this.submitted = true;
        this.is_submitting = true;
        vue.show_submitting_modal = true;
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
          console.log(JSON.stringify(response.data.request)); // eslint-disable-line
          vue.show_submitting_modal = false;
          if(response.status === 200) {
            vue.navigate_after_submit();
          }else if(response.status === 202){
            vue.show_timeout_modal = true;
          }
          vue.is_submitting = false;

        }).catch(function (error) {
          if (error.response) {
            vue.submit_msg = "Error making submission.";
          } if (error.response.status === 543){
            vue.submit_msg += " There was an issue with the AdSel API.";
          }
        });
      },
      navigate_after_submit() {
        this.$emit('show-message', "P&G assignments submitted");
        this.$router.push({path: '/log'});
      },
    }
  };
</script>

<style lang="scss">
</style>
