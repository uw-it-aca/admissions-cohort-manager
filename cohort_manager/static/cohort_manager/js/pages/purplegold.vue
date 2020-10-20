<template>
  <div>
    <h1 id="aat_page_header" class="aat-page-header">
      Assign Purple & Gold Scholarships
    </h1>
    <b-button @click="init_upload">
      Assign Scholarships
    </b-button>
    <b-button @click="init_reset">
      Reset All
    </b-button>
    <reset-modal v-if="display_reset" collection-type="purplegold" />
    <!--    <upload v-bind="currentProperties" v-on="$listeners" />-->
  </div>
</template>

<script>
  import ResetModal from "../components/reset_modal";

  export default {
    name: "PurpleGold",
    components: {
      ResetModal,
      // upload: Upload,
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
</style>
