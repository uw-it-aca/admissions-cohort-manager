<template>
  <div>
    <h2>Collection List {{ collectionType }}</h2>
    <div v-if="collectionType === 'Cohort'">
        You, Cohort, you!
        <b-table striped :items="cohorts" :fields="cohortFields">
            <template v-slot:cell(actions)="row">
                <a href="#" :title="'Assign applications to cohort ' + row.item.cohortNum">Assign</a>
                <a href="#" :title="'Activity for cohort ' + row.item.cohortNum">Activity</a>
                 <b-button size="sm" @click="info(row.item, row.index, $event.target)" :title="'Remove all assignments to cohort ' + row.item.cohortNum">Reset</b-button>
            </template>
        </b-table>
        <!-- Reset Cohort modal -->
        <b-modal :id="resetModal.id" :title="resetModal.title" ok-only @hide="resetresetModal">
          <div>This is cohort </div>
        </b-modal>
    </div>

    <div v-else-if="collectionType === 'Major'">
        You, Major, you!
        <b-table striped :items="majors" :fields="majorFields"></b-table>
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
            key: 'cohortNum',
            label: "Cohort #",
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
          { 'cohortNum': '1', Description: 'TEST: Residents, admit', Residency: 'WA-residents', Protected: 'No', Admit_Status: 'Admit', Assigned: '120'  },
          { 'cohortNum': '2', Description: 'TEST: Non-Residents, admit', Residency: 'WA-residents', Protected: 'No', Admit_Status: 'Admit', Assigned: '32'  },
          { 'cohortNum': '3', Description: 'TEST: Protected, Soccer', Residency: 'WA-residents', Protected: 'Yes', Admit_Status: 'Admit', Assigned: '0'  },
          { 'cohortNum': '99', Description: 'TEST: Lost Souls, deny', Residency: 'WA-residents', Protected: 'No', Admit_Status: 'Deny', Assigned: '1'  }
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
        resetModal: {
          id: 'reset-modal',
          title: ''
        }
      };
    },
    mounted() {
    },
    methods: {
        info(item, index, button) {
        this.resetModal.title = `Row index: ${index}`
        this.$root.$emit('bv::show::modal', this.resetModal.id, button)
      },
      resetresetModal() {
        this.resetModal.title = ''
        this.resetModal.content = ''
      },
    }
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';
  @import '../../css/custom.scss';

</style>
