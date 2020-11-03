<template>
  <div :class="'aat-globalenv-' + env">
    <env_banner v-if="env === 'localdev'" />
    <iframe_base v-if="isFrame" />
    <full_base v-else />
  </div>
</template>

<script>
  import FullBase from './full_base';
  import iFrameBase from "./iframe_base";
  import EnvBanner from "./components/env_banner";

  export default {
    name: "Base",
    components: {
      env_banner: EnvBanner,
      full_base: FullBase,
      iframe_base: iFrameBase
    },
    data(){
      return {
        env: '',
      };
    },
    computed: {
      isFrame() {
        return this.$route.path.includes("iframe");
      }
    },
    watch: {
    },
    mounted() {
      /*global aat_env*/
      this.env = aat_env;
    },
    methods: {

    }
  };
</script>

<style lang="scss">
</style>
