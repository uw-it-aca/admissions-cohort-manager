<template>
  <div>
    <h1 id="aat_page_header" class="aat-page-header">
      Purple &#38; Gold Scholarships
    </h1>
    <div v-if="!display_upload">
      <div class="aat-page-section">
        <b-button variant="primary" @click="init_upload">
          Assign Scholarships
        </b-button>
        <b-button @click="init_reset">
          Reset All
        </b-button>
      </div>
      <div class="aat-page-section">
        <p>You must be on the UW network or VPN to view this report. <a href="https://bitools.uw.edu/#/site/Production/views/PuGo/Awards?:iid=3" v-if="env === 'prod'">View in Tableau</a><a href="https://bitools.uw.edu/#/site/Transitional/views/PuGo/Awards?:iid=3" title="View in Tableau test environment" v-else>View in Tableau</a>.</p>
        <iframe src="../purplegold_embed/" class="aat-pugo-iframe" width="100%" height="800" />
      </div>
    </div>
    <reset-modal
      v-if="display_reset"
      collection-type="purplegold"
      item-id="0"
      v-on="$listeners"
    />
    <purple-gold-upload
      v-if="display_upload"
    />
  </div>
</template>

<script>
  import ResetModal from "../components/reset_modal";
  import PurpleGoldUpload from "../components/purplegold_upload";

  export default {
    name: "PurpleGold",
    components: {
      ResetModal,
      PurpleGoldUpload
    },
    data(){
      return {
        display_upload: false,
        display_reset: false
      };
    },
    computed: {},
    created (){},
    mounted() {
    },
    methods: {
      init_upload () {
        this.display_upload = true;
      },
      init_reset () {
        this.display_reset = true;
      }
    }
  };
</script>

<style lang="scss">
  .aat-pugo-iframe {
    border-style: none;
  
  }

</style>
