<template>
  <b-container fluid>
    <b-row>
      <b-col />
      <b-col>
        <b-pagination
          v-model="currentPage"
          :total-rows="totalRows"
          :per-page="perPage"
          align="right"
          size="sm"
          aria-controls="assignment_history_table"
        />
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="9">
        <b-table 
          striped 
          show-empty
          small
          stacked="md"
          id="assignment_history_table"
          class="assignment-history-table"
          :items="activities" 
          :fields="activityFields"
          :current-page="currentPage"
          :per-page="perPage"
          :filter="filter"
          :filter-included-fields="filterOn"
          @filtered="onFiltered"
        >
          <template v-slot:cell(Date)="row">
            <div>{{ row.value.day }}</div><div>{{ row.value.time }}</div>
          </template>
          <template v-slot:cell(Summary)="row">
            <div class="aat-data-split">{{ row.value.submitted }}</div><div>{{ row.value.assigned }}</div>
          </template>
        </b-table>
      </b-col>

      <b-col>
        <b-col>
          <b-form-group
            label="Assignment Type"
            label-size="sm"
            label-for="as_type_filter"
          >
            <b-input-group size="sm">
              <b-form-select
                v-model="astypeFilter"
                id="as_type_filter"
                class="aat-filter-select"
                :options="astypeOptions"
              >
                <template v-slot:first>
                  <option :value="null" disabled>
                    -- Select --
                  </option>
                </template>
              </b-form-select>
              <b-input-group-append>
                <b-button :disabled="!astypeFilter" @click="astypeFilter = ''">
                  Clear
                </b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form-group>

          <b-form-group
            label="Cohort"
            label-size="sm"
            label-for="cohort_filter"
          >
            <b-input-group size="sm">
              <b-form-select
                v-model="cohortFilter"
                id="cohort_filter"
                class="aat-filter-select"
                :options="cohortOptions"
              >
                <template v-slot:first>
                  <option :value="null" disabled>
                    -- Select --
                  </option>
                </template>
              </b-form-select>
              <b-input-group-append>
                <b-button :disabled="!cohortFilter" @click="cohortFilter = ''">
                  Clear
                </b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form-group>

          <b-form-group
            label="Major"
            label-size="sm"
            label-for="major_filter"
          >
            <b-input-group size="sm">
              <b-form-select
                v-model="majorFilter"
                id="major_filter"
                class="aat-filter-select"
                :options="majorOptions"
              >
                <template v-slot:first>
                  <option :value="null" disabled>
                    -- Select --
                  </option>
                </template>
              </b-form-select>
              <b-input-group-append>
                <b-button :disabled="!majorFilter" @click="majorFilter = ''">
                  Clear
                </b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form-group>
          
          <b-form-group
            label="System Key"
            label-size="sm"
            label-for="SysKeyInput"
          >
            <b-input-group size="sm">
              <b-form-input
                v-model="filter"
                id="SysKeyInput"
                type="search"
                placeholder="Type to Search"
              ></b-form-input>
              <b-input-group-append>
                <b-button :disabled="!filter" @click="filter = ''">
                  Clear
                </b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form-group>
        </b-col>
      </b-col>
    </b-row>
  </b-container>
</template>



<script>
  export default {
    name: "ActivityList",
    components: {
    },
    props: {
    },
    data(){
      return {
        activityFields: [
          {
            key: 'Date',
            label: "Date/Time",
            class: "aat-data-cell aat-date-cell",
            sortable: true
          },
          {
            key: 'Summary',
            class: "aat-data-cell",
            sortable: false
          },
          {
            key: 'Comment',
            class: "aat-data-cell",
            sortable: false,
          },
          {
            key: 'User',
            class: "aat-data-cell",
            sortable: false
          },
        ],
        activities: [
          { Date: { day: 'Jan. 20, 2019', time: '3:30 PM' }, Summary: { submitted: 'Submitted: Assign 3 (manual) to Cohort 41.',
assigned: 'Assigned: 3 applications to Cohort 41.' }, Comment: '“Add 3 new applications”', User: 'netid' },
          { Date: { day: 'Jan. 20, 2019', time: '12:22 PM' }, Summary: { submitted: 'Submitted: Assign 32 (manual) to Cohort 41.',
assigned: 'Assigned: 1 assigned to Cohort 2, 1 not assigned.' }, Comment: '“All res w/ overall scores of 15s added”', User: 'netid' },
        ],
        astypeFilter: null,
        astypeOptions: [
          { value: 'cohort', text: 'Cohort' },
          { value: 'major', text: 'Major' }
        ],
        cohortFilter: null,
        cohortOptions: [
          { value: '1', text: '1' },
          { value: '2', text: '2' },
          { value: '3', text: '3' },
          { value: '99', text: '99' }
        ],
        majorFilter: null,
        majorOptions: [
          { value: 'astr', text: 'ASTR' },
          { value: 'biol', text: 'BIOL' },
          { value: 'cse', text: 'CSE' },
          { value: 'hcde', text: 'HCDE' }
        ],
        totalRows: 1,
        currentPage: 1,
        perPage: 20,
        filter: null,
        filterOn: [],
      };
    },
    mounted() {
      // Set the initial number of items
      this.totalRows = this.activities.length;
    },
    methods: {
      onFiltered(filteredItems) {
        // Trigger pagination to update the number of buttons/pages due to filtering
        this.totalRows = filteredItems.length;
        this.currentPage = 1;
      }
    }
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';
  @import '../../css/custom.scss';

  .aat-filter-select {
    background: none;
  }

  .assignment-history-table {
    border-bottom: 2px solid rgba(0, 0, 0, 0.05);
    font-size: 0.85rem;
    line-height: 1.3;
  }

  table .aat-data-cell {
    padding: 1rem;

    &.aat-date-cell:first-child {
      white-space: nowrap;
    }
  }

  .aat-data-split {
    padding-bottom: 0.5rem;
  }

</style>
