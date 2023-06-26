<template>
    <div v-if="total_pages > 1" class="flex items-center justify-between mt-4 bg-white">
        <button @click="previousPage" :disabled="!has_previous"
            class="py-2 px-4 rounded-l-md  text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
            Previous
        </button>
        <span class="px-4 py-2 text-gray-700">
            Page {{ current_page }} of {{ total_pages }}
        </span>
        <button @click="nextPage" :disabled="!has_next"
            class="py-2 px-4 rounded-r-md text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
            Next
        </button>
    </div>
</template>

<script>

export default {


    props: {
        has_previous: false,
        has_next: false,
        total_pages: 0,
        current_page: 0,
    },

    emits: ['getFeed'],

    methods: {

        previousPage() {
            if (this.has_previous) {
                this.$emit('getFeed', this.current_page - 1)
            }
        },
        nextPage() {
            if (this.has_next) {
                this.$emit('getFeed', this.current_page + 1)
            }
        },
    }
}
</script>
