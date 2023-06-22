<template>
    <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <h2 class="text-lg mb-4">Trends</h2>
        <div class="flex flex-col space-y-2 justify-between">
            <div v-for="trend in trends" :key="trend.hashtag" class="flex justify-between items-center text-sm">
                <div class="flex flex-col justify-center">
                    <p class=" font-bold text-xs">#{{ trend.hashtag }}</p>
                    <p class="text-gray-500 text-xs">{{ trend.occurences }} posts</p>
                </div>
                <RouterLink :to="{ name: 'trenddetail', params: { hashtag: trend.hashtag } }">
                    <div class="text-white px-3 py-2 bg-purple-800 rounded-lg">Explore</div>
                </RouterLink>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'trend',

    data() {
        return {
            trends: [],
        }
    },

    mounted() {
        this.getTrend();
    },

    methods: {
        getTrend() {
            console.log('getTrend');
            axios
                .get('api/post/trend/')
                .then(response => {
                    console.log(response.data);
                    this.trends = response.data;
                })
                .catch(err => {
                    console.log(err);
                })
        },


    }


}

</script>