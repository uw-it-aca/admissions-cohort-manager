<template>
  <div>
    <b-modal
      ref="submitting_modal"
      modal-class="aat-modal-box"
      content-class="aat-modal"
      hide-backdrop
      :hide-footer="true"
      :hide-header="true"
      :hide-header-close="true"
      :no-close-on-backdrop="true"
      :no-close-on-esc="true"
    >
      <div class="text-center text-info aat-processing-text">
        <b-spinner class="align-middle" />
        <strong>Processing...</strong>
      </div>
      <p class="text-center aat-processing-message">
        Please wait while your submission is processed.
      </p>
    </b-modal>
    <b-modal
      ref="submitting_timeout_modal"
      modal-class="aat-modal-box"
      content-class="aat-modal"
      hide-backdrop
      :hide-header="true"
      :ok-only="true"
      ok-title="Close"
      :no-close-on-backdrop="true"
      :no-close-on-esc="true"
      @ok="navigate_after_submit"
    >
      <h1 class="aat-sub-header">
        The AdSel Database is not responding
      </h1>
      <div class="aat-processing-message">
        <p>If assigning a large number of applications, the AdSel Db could still be processing your submission.</p>
        <p>
          Please check the <b-link to="/log/">
            Activity Log
          </b-link> in a few minutes to ensure your submission was completed.
        </p>
      </div>
    </b-modal>
  </div>
</template>

<script>
  export default {
    name: "CollectionSubmitModal",
    components: {
    },
    props: {
      showSubmitting: {
        type: Boolean,
        default: false
      },
      showTimeout: {
        type: Boolean,
        default: false
      },
    },
    data() {
      return {};
    },
    watch: {
      showSubmitting: function () {
        if(this.showSubmitting){
          this.$refs['submitting_modal'].show();
        } else {
          this.$refs['submitting_modal'].hide();
        }
      },
      showTimeout: function () {
        if(this.showTimeout){
          this.$refs['submitting_timeout_modal'].show();
        } else {
          this.$refs['submitting_timeout_modal'].hide();
        }
      }
    },
    methods: {
      navigate_after_submit(){
        this.$router.push({path: '/log'});
      }
    }
  };
</script>

<style lang="scss">
</style>
