<template>
  <div>
    <b-modal
      id="reset-modal"
      v-model="show_modal"
      modal-class="aat-modal-box"
      content-class="aat-modal"
      hide-backdrop
      :title="'Reset ' + typeDisplay"
      ok-only
      :ok-title="'Reset ' + typeDisplay"
      :ok-disabled="okDisabled"
      @ok="handleReset"
    >
      <form @submit.prevent="handleReset">
        <div>
          <fieldset class="aat-form-section">
            <legend class="aat-sub-header">
              Confirm Reset
            </legend>
            <div id="reset_col_option">
              <b-form-checkbox
                id="col_reset_checkbox"
                v-model="confirm_reset"
                name="col_reset_checkbox"
                :value="true"
              >
                <span v-if="collectionType === 'purplegold'">
                  Reset all Purple &#38; Gold scholarship assignments for <strong>{{ periodText }}</strong>.
                </span>
                <span v-else>
                  Reassign all applications from "<span v-if="collectionType === 'Cohort'">Cohort </span>{{ itemId }}" to <em>unassigned</em>.
                </span>
              </b-form-checkbox>
            </div>
          </fieldset>
          <fieldset class="aat-form-section">
            <legend class="aat-sub-header">
              Add Comment
            </legend>
            <label for="reassignment_comment">Enter comment for this assignment.</label>
            <textarea id="reassignment_comment" v-model="comment" class="aat-comment-field" />
          </fieldset>
          <p v-if="protectedCohort">
            <b>Note:</b> This is a protected cohort.
          </p>
        </div>
      </form>
      <div v-if="is_resetting" class="text-center text-info aat-processing-text">
        <b-spinner class="align-middle" />
        <strong>Resetting...</strong>
      </div>
    </b-modal>
  </div>
</template>

<script>
  import Vuex from "vuex";

  const axios = require("axios");
  export default {
    name: "ResetModal",
    components: {
    },
    props: {
      collectionType: {
        type: String,
        default: ""
      },
      itemId: {
        type: String,
        default: ""
      },
      protectedCohort: {
        type: Boolean,
        default: function () {
          return false;
        }
      },
    },
    data() {
      return {
        id: '',
        show_modal: true,
        is_resetting: false,
        confirm_reset: false,
        comment: "",
        csrfToken: ""
      };
    },
    computed: {
      typeDisplay: function () {
        if(this.collectionType === "purplegold"){
          return "Purple & Gold Scholarships";
        } else {
          return this.collectionType;
        }
      },
      okDisabled: function() {
        if(this.is_resetting){
          return true;
        } else {
          return !this.confirm_reset;
        }
      },
      ...Vuex.mapState({
        current_period: state => state.period.current_period
      }),
      periodText: function() {
        return $cookies.get('session_period_text');
      }
    },
    mounted() {
      this.setCSRF();
    },
    methods: {
      setCSRF() {
        this.csrfToken = $cookies.get("csrftoken");
      },
      handleReset(bvModalEvent) {
        var vue = this;
        // disable submit after click
        bvModalEvent.preventDefault();
        this.is_resetting = true;
        axios.delete(
          '/api/collection/'
            + this.collectionType.toLowerCase()
            + "/"
            + this.current_period
            + "/"
            + this.itemId
            + "/",
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              'X-CSRFToken': this.csrfToken
            },
            data: {comment: this.comment}
          },
        ).then(function() {
          bvModalEvent.vueTarget.hide();
          vue.is_resetting = false;
          vue.$emit('show-message', vue.collectionType + " " + vue.itemId + " has been reset.", "success");
          vue.$router.push({path: '/log'});
        }).catch(function () {
          bvModalEvent.vueTarget.hide();
          vue.is_resetting = false;
          vue.$emit('show-message', "Reset of " + vue.collectionType + " " + vue.itemId + " has been submitted. Changes may take a few minutes to update in the Activity Log.", "primary");
          vue.$router.push({path: '/log'});
        });

      },
    }
  };
</script>

<style lang="scss">
</style>
