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
          id="assignment_history_table"
          striped
          show-empty
          small
          class="aat-data-table"
          stacked="md"
          :items="activities"
          :fields="activityFields"
          :current-page="currentPage"
          :per-page="perPage"
          :filter="filter"
          :filter-included-fields="filterOn"
          @filtered="onFiltered"
        >
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
                id="as_type_filter"
                v-model="astypeFilter"
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
                id="cohort_filter"
                v-model="cohortFilter"
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
                id="major_filter"
                v-model="majorFilter"
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
                id="SysKeyInput"
                v-model="filter"
                type="search"
                placeholder="Type to Search"
              />
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
  const axios = require("axios");
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
            key: 'activity_date',
            label: "Date/Time",
            class: "aat-data-cell aat-data-nowrap",
            sortable: true
          },
          {
            key: 'assigned_msg',
            class: "aat-data-cell",
            sortable: false
          },
          {
            key: 'submitted_msg',
            class: "aat-data-cell",
            sortable: false
          },
          {
            key: 'Comment',
            class: "aat-data-cell",
            sortable: false,
          },
          {
            key: 'user',
            class: "aat-data-cell",
            sortable: false
          },
        ],
        activities: [],
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
      this.getAllActivities();
    },
    methods: {
      onFiltered(filteredItems) {
        // Trigger pagination to update the number of buttons/pages due to filtering
        this.totalRows = filteredItems.length;
        this.currentPage = 1;
      },
      getAllActivities() {
        axios.get(
          '/api/activity/',
        ).then(response => {
          if(response.status === 200){
            this.activities = response.data.activities;
          }
        });

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

</style>
