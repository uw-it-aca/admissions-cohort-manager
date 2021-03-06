<template>
  <div>
    <form @submit.prevent="">
      <div class="aat-form-section">
        <fieldset class="aat-collection-select">
          <legend class="aat-sub-header">
            Select {{ collectionType }}
          </legend>
          <label for="input-with-list">Assign applications to <span v-if="collectionType === 'Cohort'">cohort</span><span v-else>major</span></label>
          <div v-if="hasCollections" class="aat-select-inline">
            <b-form-input id="input-with-list"
                          v-model="collection_id"
                          autocomplete="off"
                          list="input-list"
                          required
                          :disabled="loadingCollection || has_uploaded"
                          :class="{'is-invalid': !collection_id}"
            />
            <b-form-invalid-feedback true>
              Please select an option.
            </b-form-invalid-feedback>
            <b-form-datalist id="input-list" :options="computedCollectionOptions" />
          </div>
          <div v-else>
            <div class="alert alert-danger" role="alert">
              No {{ collectionType }}s found for selected period.
            </div>
          </div>
        </fieldset>
        <div class="aat-collection-note">
          Please confirm {{ collectionType.toLowerCase() }} information is correct before entering applications.
        </div>
        <div role="region" aria-live="polite">
          <collectionDetails
            v-if="show_details"
            :collection-id="collection_id"
            :collection-type="collectionType"
            :current-period="currentPeriod"
            :periods="periods"
          />
        </div>
      </div>
      <div v-if="collection_id !== null">
        <fieldset class="aat-form-section">
          <legend class="aat-sub-header">
            Enter Applications
          </legend>
          <div id="add_applications_widget">
            <div v-if="!has_uploaded">
              <div>
                <b-spinner v-if="is_uploading && invalid_upload === false" class="text-center" label="Submitting your assignments" />
                <span v-else>
                  Enter applications by file (csv) or
                  <b-button id="manual_toggle" v-b-modal.add_list_modal class="aat-btn-link" variant="link">
                    {{ uploadToggleLabel }}
                  </b-button>
                </span>
                <CollectionUploadListInput @listupdated="selectedList" />
              </div>
              <component
                :is="uploadComponent"
                @fileuploaded="selectedFile"
                @fileerror="fileError"
              />
            </div>
            <upload-review v-else
                           :upload-response="syskey_upload_response"
                           :collection-type="collection_type"
                           :upload-type="manual_upload ? 'list' : 'file'"
                           :collection-options="collectionOptions"
                           :collection-id="collection_id"
                           @upload-reset="handleReset"
                           @is-reassign="handle_reassign"
                           @is-reassign-protected="handle_reassign_protected"
            />
            <collection-upload-dupe-modal
              v-if="has_dupes"
              :duplicates="dupes"
              :collection-type="collectionType"
              @remove-dupes="remove_applications"
            />
          </div>
          <b-alert id="add_app_fail_manual" :show="invalid_manual" variant="danger">
            The following system keys are invalid:
            <ul class="att-error-list">
              <li
                v-for="value in invalid_syskeys"
                :key="value.id"
              >
                {{ value }}
              </li>
            </ul>
            You will need to correct these before moving forward.
          </b-alert>
          <b-alert id="add_app_fail_csv" :show="file_invalid" variant="danger">
            CSV is invalid. {{ file_invalid_msg }}
          </b-alert>
        </fieldset>
        <collection-comment
          @comment="update_comment"
        />
        <b-button type="submit" variant="primary" :disabled="is_disabled_submit_button" @click="mark_for_submission">
          Submit
        </b-button>
        <collection-submit-modal
          :show-submitting="show_submitting_modal"
          :show-timeout="show_timeout_modal"
        />
        <p>{{ submit_msg }}</p>
      </div>
    </form>
  </div>
</template>

<script>
  const axios = require("axios");
  import CollectionDetails from "../components/collection_details.vue";
  import CollectionUploadListInput from "../components/collection_upload_list_input.vue";
  import CollectionUploadFileInput from "../components/collection_upload_file_input.vue";
  import CollectionUploadDupeModal from "../components/collection_upload_dupe_modal.vue";
  import UploadReview from "../components/collection_upload_review.vue";
  import CollectionComment from "../components/collection_comment.vue";
  import CollectionSubmitModal from "../components/collection_submit_modal";
  import Vue from "vue/dist/vue.esm.js";
  import VueCookies from "vue-cookies";
  Vue.use(VueCookies);
  export default {
    name: "Upload",
    components: {
      CollectionUploadDupeModal,
      collectionDetails: CollectionDetails,
      uploadReview: UploadReview,
      CollectionUploadListInput: CollectionUploadListInput,
      CollectionUploadFileInput: CollectionUploadFileInput,
      CollectionComment: CollectionComment,
      CollectionSubmitModal
    },
    props: {
      collectionType: {
        type: String,
        default: ""
      },
      collectionOptions: {
        type: Array,
        default: function () {return[];}
      },
      currentPeriod: {
        type: Number,
        default: null
      },
      loadingCollection: {
        type: Boolean,
        default: true
      },
      periods: {
        type: Array,
        default: function () {return[];}
      }
    },
    data(){
      return {
        file_data: null,
        file_invalid: false,
        file_invalid_msg: "",
        filename: undefined,
        syskey_list: null,
        syskey_upload_response: null,
        collection_id: null,
        comment: '',
        csrfToken: '',
        manual_upload: false,
        upload_toggle_label_file: "by file",
        upload_toggle_label_manual: "manually by system keys",
        has_uploaded: false,
        has_dupes: false,
        dupes: [],
        upload_response: undefined,
        collection_type: this.$props.collectionType,
        to_remove: [],
        is_reassign: false,
        is_reassign_protected: false,
        invalid_syskeys: [],
        submitted: false,
        is_uploading: false,
        is_submitting: false,
        submit_msg: "",
        show_submitting_modal: false,
        show_timeout_modal: false
      };
    },
    computed: {
      uploadComponent: function () {
        if (this.manual_upload) {
          return "CollectionUploadListInput";
        } else {
          return "CollectionUploadFileInput";
        }
      },
      uploadToggleLabel: function() {
        if (!this.manual_upload) {
          return this.upload_toggle_label_manual;
        } else {
          return this.upload_toggle_label_file;
        }
      },
      computedCollectionOptions: function() {
        var list = [];
        $.each(this.collectionOptions, function (idx, option) {
          var new_title_opt = {...option};
          new_title_opt['text'] = new_title_opt['value'] + ": " + new_title_opt['text'];
          list.push(new_title_opt);
        });
        return list;
      },
      is_disabled_submit_button: function() {
        return this.submitted === false && this.has_uploaded === false;
      },
      invalid_upload: function() {
        return this.invalid_manual;
      },
      hasCollections: function () {
        return this.collectionOptions.length > 0;
      },
      show_details: function () {
        return (this.collectionType === 'Cohort' || this.collectionType === 'Major')
          && this.collection_id != null && this.collection_id.length > 0;
      },
      invalidSyskeys: function() {
        var invalid_syskeys = [];
        if (this.syskey_upload_response){
          for (let app of this.syskey_upload_response.assignments) {
            if(app.application_not_found){
              invalid_syskeys.push(app.system_key);
            }
          }
        }
        return invalid_syskeys;
      },
      invalid_manual: function(){
        return this.manual_upload && this.invalidSyskeys.length > 0;
      }
    },
    watch: {
      collectionOptions: function(){
        if (this.$route.params.id !== undefined) {
          this.selectCollection(this.$route.params.id);
        }
      },
      file_data: function(val){
        this.file_invalid = this.validateFileData(val);
        if(!this.file_invalid){
          this.handleSyskeyUpload();
        }
      },
      syskey_upload_response: function(val){
        if(val !== undefined){
          var dupes = this.get_duplicates(val.assignments);
          if(dupes.length > 0) {
            this.has_dupes = true;
            this.dupes = dupes;
          }
          var invalid_syskeys = this.invalidSyskeys;
          if(invalid_syskeys.length > 0){
            this.invalid_syskeys = invalid_syskeys;
          }
        }
      }
    },
    mounted() {
      if (this.$route.params.id !== undefined) {
        this.selectCollection(this.$route.params.id);
      }
      this.setCSRF();
    },
    methods: {
      setCSRF() {
        this.csrfToken = $cookies.get("csrftoken");
      },
      handleReset() {
        this.has_uploaded = false;
        this.upload_response = undefined;
        this.syskey_list = null;
        this.upload_response = null;
        this.has_dupes = false;
        this.dupes = null;
        this.manual_upload = false;
        this.file_invalid = false;
        this.filename = undefined;
        this.is_uploading = false;
      },
      handleSyskeyUpload() {
        const vue = this;
        let request = {
          'comment': this.comment,
          'qtr_id': this.currentPeriod,
          'syskey_list': this.syskey_list,
          'file_name': this.filename
        };
        if (this.collectionType == "Cohort") {
          request['cohort_id'] = this.collection_id;
        } else if (this.collectionType == "Major") {
          request['major_id'] = this.collection_id;
        }
        this.is_uploading = true;
        axios.post(
          '/api/syskeyupload',
          request,
          {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': this.csrfToken
            }
          }
        ).then(function(response) {
          vue.syskey_upload_response = response.data;
          vue.has_uploaded = true;
          vue.is_uploading = false;
        });

      },
      handle_reassign(is_reassign){
        this.is_reassign = is_reassign;
      },
      handle_reassign_protected(is_reassign_protected){
        this.is_reassign_protected = is_reassign_protected;
      },
      mark_for_submission(){
        var vue = this,
            request = {'is_submitted': true,
                       'is_reassign': this.is_reassign,
                       'is_reassign_protected': this.is_reassign_protected,
                       'to_delete': this.to_remove,
                       'comment': this.comment};
        this.submitted = true;
        this.is_submitting = true;
        vue.show_submitting_modal = true;
        if (this.collectionType == "Cohort") {
          request.cohort_id = this.collection_id;
        } else if (this.collectionType == "Major") {
          request.major_id = this.collection_id;
        }
        axios.put(
          '/api/syskeyupload/' + this.syskey_upload_response.id + "/",
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
        if(this.collection_type == "Cohort"){
          this.$emit('show-message', "Assignment to Cohort " + this.collection_id + " submitted");
          this.$router.push({path: '/log'});
        } else if(this.collection_type == "Major"){
          this.$emit('', "Assignment to " + this.collection_id + " submitted");
          this.$router.push({path: '/log'});
        }
      },

      remove_applications(list){
        var vue = this,
            request = {'submit': false,
                       'is_reassign': false,
                       'is_reassign_protected': false,
                       'to_delete': list};
        axios.put(
          '/api/syskeyupload/' + this.syskey_upload_response.id + "/",
          request,
          {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': this.csrfToken
            }
          }
        ).then(function(response) {
          vue.syskey_upload_response = response.data;
          vue.has_uploaded = true;
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
      selectedList(list) {
        this.syskey_list = list;
        this.manual_upload = true;
        this.handleSyskeyUpload();
      },
      selectedFile(file_data) {
        this.handleReset();
        this.syskey_list = file_data.syskeys;
        this.filename = file_data.filename;
        this.handleSyskeyUpload();
      },
      fileError(error){
        this.file_invalid = true;
        this.file_invalid_msg = error;
      },
      selectCollection(id){
        // Only allow options that are in list
        var id_to_set;
        $(this.collectionOptions).each(function(idx, option){

          if (id === option.value.toString()){
            id_to_set = id;
          }
        });
        if (id_to_set !== undefined){
          this.collection_id = id_to_set;
        }
      },
      update_comment(comment){
        this.comment = comment;
      }
    }
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';

  // form fields
  .aat-file-input {
    padding: 1rem 0;
  }

  .aat-collection-select {
    .aat-collection-select-label {
      display: inline-block;
      margin-right: 0.5rem;
    }

    .aat-select-inline {
      display: inline-grid;
      margin-left: 0.25rem;
    }
  }

  // form messaging
  .aat-collection-note {
    margin-bottom: 0;
    margin-top: 2rem;
  }

  .aat-status-feedback {
    margin-bottom: 0;
    padding-top: 0.5rem;
  }

  .aat-application-count {
    display: block;
    font-weight: bold;
    margin-bottom: 0.5rem;
    padding-top: 1rem;
  }

  .aat-assigned-count {
    margin-left: 0.5rem;
  }

  .alert-danger {
    max-width: 650px;
  }

  .att-error-list {
    margin-top: 1rem;
  }

  // action elements
  .aat-btn-link {
    padding: 0 !important;
    vertical-align: baseline !important;
  }

</style>
