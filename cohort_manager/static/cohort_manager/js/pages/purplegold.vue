<template>
  <div>
    <h1 id="aat_page_header" class="aat-page-header">
      Assign Purple &#38; Gold Scholarships
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
        <h2 class="aat-sub-header">
          Tableau Embedded Report
        </h2>
        <p>You must be on the UW network or VPN to access view embedded report</p>
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
