<template>
  <div>
    <h1 id="aat_page_header" class="aat-page-header">
      Assign to Cohort
    </h1>
    <upload v-bind="currentProperties" v-on="$listeners" />
  </div>
</template>

<script>
  import Upload from "../components/collection_upload.vue";
  import { EventBus } from "../main";
  const axios = require("axios");

  export default {
    name: "Cohort",
    components: {
      upload: Upload,
    },
    data(){
      return {
        has_uploaded: false,
        upload_response: undefined,
        cohort_options: [
        ],
        current_period: null
      };
    },
    computed: {
      currentComponent: function () {
        if(this.has_uploaded){
          return "uploadReview";
        } else {
          return "upload";
        }

      },
      currentProperties: function() {
        var properties = {collectionType: 'Cohort'};
        if(this.has_uploaded){
          properties['uploadResponse'] = this.upload_response;
        }
        properties['collectionOptions'] = this.cohort_options;
        properties['uploadResponse'] = this.upload_response;
        properties['currentPeriod'] = this.current_period;
        return properties;
      }
    },
    created (){
      this.current_period = this.$attrs.cur_period;
      this.get_cohorts_for_period();
      EventBus.$on('period_change', period => {
        this.current_period = period;
        this.get_cohorts_for_period();
      });
    },
    mounted() {
    },
    methods: {
      get_cohorts_for_period(){
        axios.get(
          '/api/collection/cohort/' + this.current_period + "/"
        ).then(response => {
          this.cohort_options = response.data;
        });
      },
      onFileUpload(response){
        this.has_uploaded = true;
        this.upload_response = response.data;
      }
    }
  };
</script>

<style lang="scss">
</style>
