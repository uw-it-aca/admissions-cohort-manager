<template>
  <div>
    <h2>Collection List {{ collectionType }}</h2>
    <div v-if="collectionType === 'Cohort'">
        You, Cohort, you!
        <b-table hover :items="cohorts" :fields="cohortFields">
            <template v-slot:cell(actions)="row">
                <a href="http://www.google.com">search</a>
            </template>
        </b-table>
    </div>

    <div v-else-if="collectionType === 'Major'">
        You, Major, you!
        <b-table hover :items="majors" :fields="majorFields"></b-table>
        </div>

    <div v-else>
        Error: There was an issue with your request. Please select a link from the left column to try again.
        </div>
  </div>

</template>

<script>
  export default {
    name: "CollectionList",
    components: {
    },
    props: {
      collectionType: {
        type: String,
        default: ""
      },
    },
    data(){
      return {
        cohortFields: [
          {
            key: 'cohort_#',
            sortable: true
          },
          {
            key: 'Description',
            sortable: true
          },
          {
            key: 'Residency',
            sortable: true,
          },
          {
            key: 'Protected',
            sortable: true
          },
          {
            key: 'Admit_Status',
            sortable: true
          },
          {
            key: 'Assigned',
            sortable: true,
          },
          { key: 'actions', label: 'Actions' }
        ],
        cohorts: [
          { 'cohort_#': '1', Description: 'TEST: Residents, admit', Residency: 'WA-residents', Protected: 'No', Admit_Status: 'Admit', Assigned: '120'  },
          { 'cohort_#': '2', Description: 'TEST: Non-Residents, admit', Residency: 'WA-residents', Protected: 'No', Admit_Status: 'Admit', Assigned: '32'  },
          { 'cohort_#': '3', Description: 'TEST: Protected, Soccer', Residency: 'WA-residents', Protected: 'Yes', Admit_Status: 'Admit', Assigned: '0'  },
          { 'cohort_#': '99', Description: 'TEST: Lost Souls, deny', Residency: 'WA-residents', Protected: 'No', Admit_Status: 'Deny', Assigned: '1'  }
        ],
        majorFields: [
          {
            key: 'Major',
            sortable: true
          },
          {
            key: 'Division',
            sortable: true
          },
          {
            key: 'College',
            sortable: true,
          },
          {
            key: 'DTX',
            sortable: true
          },
          {
            key: 'Assigned',
            sortable: true
          },
          {
            key: 'Actions',
            label: '',
            sortable: false,
          }
        ],
        majors: [
          { Major: 'TEST: American ethnic studies', Division: 'Humanities', College: 'Arts and Sciences', DTX: 'No', Assigned: '0' },
          { Major: 'Anthropology', Division: 'Humanities', College: 'Arts and Sciences', DTX: 'No', Assigned: '134' },
          { Major: 'Aquatic & fishery sciences', Division: 'Natural Sciences', College: 'Arts and Sciences', DTX: 'No', Assigned: '12' },
          { Major: 'Engineering undeclared', Division: 'Humanities', College: 'College of Engineering', DTX: 'Yes', Assigned: '322' }
        ],
        infoModal: {
          id: 'info-modal',
          title: '',
          content: ''
        }
      };
    },
    mounted() {
    },
    methods: {
        info(item, index, button) {
        this.infoModal.title = `Row index: ${index}`
        this.infoModal.content = JSON.stringify(item, null, 2)
        this.$root.$emit('bv::show::modal', this.infoModal.id, button)
      },
      resetInfoModal() {
        this.infoModal.title = ''
        this.infoModal.content = ''
      },
    }
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';
  @import '../../css/custom.scss';

</style>
