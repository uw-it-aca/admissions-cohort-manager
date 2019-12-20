<template>
  <div>
    <form @submit.prevent="">
      <div class="aat-form-section">
        <fieldset class="aat-collection-select">
          <legend class="aat-sub-header">
            Select {{ collectionType }}
          </legend>
          <label for="input-with-list">Assign applications to {{ collectionType }} </label>
          <div class="aat-select-inline">
            <b-form-input id="input-with-list"
                          v-model="collection_id"
                          list="input-list"
                          required
                          :class="{'is-invalid': !collection_id}"
            />
            <b-form-invalid-feedback true>
              Please select an option.
            </b-form-invalid-feedback>
            <b-form-datalist id="input-list" :options="collectionOptions" />
          </div>
        </fieldset>
        <div role="region" aria-live="polite">
          <collectionDetails
            v-if="collectionType === 'Cohort'"
            :collection-id="collection_id"
            :collection-type="collectionType"
            :current-period="currentPeriod"
          />
        </div>
      </div>
      <fieldset class="aat-form-section">
        <legend class="aat-sub-header">
          Enter Applications
        </legend>
        <div id="add_applications_widget">
          <upload-review v-if="has_uploaded"
                         :upload-response="upload_response"
                         :collection-type="collection_type"
                         :upload-type="manual_upload ? 'list' : 'file'"
                         :collection-options="collectionOptions"
                         @upload_reset="handleReset"
                         @is_reassign="handle_reassign"
                         @is_reassign_protected="handle_reassign_protected"
          />
          <div v-else>
            <div>
              Enter applications by file (csv) or
              <b-button id="manual_toggle" v-b-modal.add_list_modal class="aat-btn-link" variant="link">
                {{ uploadToggleLabel }}
              </b-button>
              <CollectionUploadListInput @listupdated="selectedList" />
            </div>
            <component
              :is="uploadComponent"
              @fileselected="selectedFile"
            />
          </div>
          <collection-upload-dupe-modal
            v-if="has_dupes"
            :duplicates="dupes"
            :collection-type="collectionType"
            @removeDupes="remove_applications"
          />
        </div>
        <b-alert id="add_app_fail_manual" :show="invalid_manual" variant="danger">
          Invalid systems keys.
        </b-alert>
        <b-alert id="add_app_fail_csv" :show="invalid_csv" variant="danger">
          CSV is invalid.
        </b-alert>
      </fieldset>
      <fieldset class="aat-form-section">
        <legend class="aat-sub-header">
          Add Comment
        </legend>
        <label for="assignment_comment">Enter comment for this assignment</label>
        <textarea id="assignment_comment" v-model="comment" class="aat-comment-field" />
      </fieldset>
      <b-button type="submit" variant="primary" @click="mark_for_submission">
        Submit
      </b-button>
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
        type: String,
        default: null
      }
    },
    data(){
      return {
        file: null,
        syskey_list: null,
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
        invalid_manual: false,
        invalid_csv: false
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
        this.file = null;
        this.syskey_list = null;
        this.upload_response = null;
        this.has_dupes = false;
        this.dupes = null;
        this.manual_upload = false;
      },
      handleUpload() {
        var vue = this;
        let formData = new FormData();
        // Reset error modals
        this.invalid_csv = false;
        this.invalid_manual = false;

        if (this.file !== null){
          this.manual_upload = false;
          formData.append('file', this.file);
        } else  if (this.syskey_list !== null){
          this.manual_upload = true;
          formData.append('syskey_list', this.syskey_list);
        }
        formData.append('comment', this.comment);
        formData.append('qtr_id', this.currentPeriod);
        if (this.collectionType == "Cohort") {
          formData.append('cohort_id', this.collection_id);
        } else if (this.collectionType == "Major") {
          formData.append('major_id', this.collection_id);
        } else {
          this.uploadResponse = "THERE WAS AN ERROR";
          return;
        }
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
          vue.upload_response = response.data;
          var dupes = vue.get_duplicates(this.upload_response.assignments);
          if(dupes.length > 1){
            vue.has_dupes = true;
            vue.dupes = dupes;
          } else{
            vue.has_uploaded = true;
          }
        }).catch(function () {
          if(vue.file !== null){
            vue.invalid_csv = true;
            vue.handleReset();
          }else if(vue.syskey_list!==null){
            vue.invalid_manual = true;
            vue.handleReset();
          }
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
        axios.put(
          '/api/upload/' + this.upload_response.id + "/",
          request,
          {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': this.csrfToken
            }
          }
        ).then(function() {
          if(vue.collection_type == "Cohort"){

            vue.$emit('showMessage', "Cohort " + vue.collection_id);
            vue.$router.push({path: '/cohort_list'});
          } else if(vue.collection_type == "Major"){
            vue.$emit('showMessage', vue.collection_id);
            vue.$router.push({path: '/major_list'});
          }


        });
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
      selectedFile(file) {
        this.file = file;
        this.handleUpload();
      },
      selectedList(list) {
        this.syskey_list = list;
        this.handleUpload();
      },
      selectCollection(id){
        // Only allow options that are in list
        var id_to_set;
        $(this.collectionOptions).each(function(idx, option){
          if (id === option.value){
            id_to_set = id;
          }
        });
        if (id_to_set !== undefined){
          this.collection_id = id_to_set;
        }
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

  .aat-comment-field {
    display: block;
    height: 144px;
    max-width: 650px;
    min-width: 250px;
    padding: 0.5rem;
    width: 100%;
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
  .aat-status-feedback {
    padding-top: 0.5rem;
  }

  .alert-danger {
    max-width: 650px;
  }

  // action elements
  .aat-btn-link {
    padding: 0 !important;
    vertical-align: baseline !important;
  }

</style>
