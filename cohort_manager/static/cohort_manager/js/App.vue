<template>
  <div>
    <env_banner />
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
    },
    methods: {

    }
  };
</script>

<style lang="scss">
</style>
