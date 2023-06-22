<template>
    <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <h2 class="text-lg mb-4">People you may know</h2>
        <div class="flex flex-col space-y-2 justify-between">
            <div v-for="user in users" class="flex justify-between items-center text-sm">
                <div class="flex items-center justify-between space-x-2">
                    <img class="w-[40px] rounded-full" :src="user.get_avatar" alt="">
                    <p class="font-bold">{{ user.name }}</p>
                </div>
                <a href="">
                    <RouterLink :to="{ name: 'profile', params: { id: user.id } }"
                        class="text-white px-3 py-2 bg-purple-800 rounded-lg">Show</RouterLink>
                </a>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            users: []
        }
    },

    mounted() {
        this.getUsers()
    },

    methods: {
        getUsers() {
            console.log('getUsers')

            axios
                .get('api/people_you_may_know/',)
                .then(response => {
                    console.log(response.data)

                    this.users = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }
}
</script>