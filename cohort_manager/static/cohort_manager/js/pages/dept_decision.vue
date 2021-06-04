<template>
  <div>
    <h1 id="aat_page_header" class="aat-page-header">
      Assign Departmental Decision {{ dd_number }}
    </h1>
    <upload
      v-if="validDDNumber"
      v-bind="currentProperties"
      v-on="$listeners"
    />
    <p v-else>
      Invalid Dept Decision number supplied, may only assign to 1 or 2
    </p>
  </div>
</template>

<script>
  import Upload from "../components/collection_upload.vue";
  import { EventBus } from "../main";
  const axios = require("axios");

  export default {
    name: "DeptDecision",
    components: {
      upload: Upload,
    },
    data(){
      return {
        dd_number: undefined,
        has_uploaded: false,
        upload_response: undefined,
        dd_options: [],
        current_period: undefined,
        loading_collection: true,
        periods: []
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
        var properties = {collectionType: 'DD'};
        if(this.has_uploaded){
          properties['uploadResponse'] = this.upload_response;
        }
        properties['collectionOptions'] = this.dd_options;
        properties['currentPeriod'] = this.current_period;
        properties['loadingCollection'] = this.loading_collection;
        properties['periods'] = this.periods;
        return properties;
      },
      validDDNumber: function () {
        return this.dd_number === 1 || this.dd_number === 2;
      }
    },
    watch: {
      '$route.params.dd_number': function (dd_number) {
        this.dd_number = parseInt(dd_number);
      }
    },
    created (){
      this.current_period = this.$attrs.cur_period;
      this.periods = this.$attrs.periods;
      this.get_dd_options_for_period();
      EventBus.$on('period-change', period => {
        this.current_period = period;
        this.get_dd_options_for_period();
      });
    },
    mounted() {
      this.dd_number = parseInt(this.$route.params.dd_number);
      this.get_dd_options_for_period();
    },
    methods: {
      get_dd_options_for_period(){
        this.loading_collection = true;
        axios.get(
          '/api/collection/dd/' + this.current_period + "/"
        ).then(response => {
          this.loading_collection = false;
          this.dd_options = response.data;
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

