<template>
  <b-modal modal-class="aat-modal-box" content-class="aat-modal" hide-backdrop id="dupe_list_modal" ref="dupe_modal" title="Duplicate Applications Found" ok-title="Done" @ok="removeDupes" no-close-on-backdrop="true" no-close-on-esc="true" >
    <div>
      <b-card-text>
        Select the applications that you want to assign:
      </b-card-text>
      <b-card-text>
        <applicationlist
          application-return="Duplicate"
          :collection-type="collectionType"
          :applications="duplicates"
          @dupeToRemove="dupeManager"
        />
      </b-card-text>
    </div>
  </b-modal>
</template>

<script>
  import ApplicationList from "../components/application_list.vue";
  export default {
    name: "CollectionUploadDupeModal",
    components: {
      applicationlist : ApplicationList
    },
    props: {
      duplicates: {
        type: Array,
        default: function () {return[];}
      },
      collectionType: {
        type: String,
        default: ""
      },
    },
    data(){
      return {
        to_remove: []
      };
    },
    mounted() {
      this.$refs.dupe_modal.show();
    },
    methods: {
      dupeManager(list) {
        // Something is causing this to fire when modal closes,
        // ignore that object
        if(Array.isArray(list)){
          this.to_remove = list;
        }
        return;
      },
      removeDupes(){
        this.$emit('removeDupes', this.to_remove);
      }
    }
  };
</script>

<style lang="scss">
</style>
