<template>
    <div class="mx-auto max-w-7xl grid grid-cols-2 gap-4">
        <div class="main-left cols-span-1 bg-white rounded-lg border-gray-300 px-10 py-12 space-y-8">
            <h2 class="text-2xl font-semibold">Log in</h2>
            <p class="text-gray-500">Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                Lorem ipsum dolor sit
                mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.</p>
            <p class="font-bold">Don't have an account? <RouterLink :to="{ 'name': 'signup' }" class="underline">Click here
                </RouterLink> to create one!</p>
        </div>
        <div class="main-right cols-span-1 bg-white rounded-lg border-gray-300 px-10 py-12">
            <form class="space-y-6" v-on:submit.prevent="submitForm">
                <div>
                    <label>E-mail</label><br>
                    <input type="email" v-model="form.email" placeholder="Your e-mail address"
                        class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                </div>

                <div>
                    <label>Password</label><br>
                    <input type="password" v-model="form.password" placeholder="Your password"
                        class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                </div>

                <template v-if="errors.length > 0">
                    <div class="bg-red-300 text-white rounded-lg p-6">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>
                </template>

                <div>
                    <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Log in</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            errors: []
        }
    },
    methods: {
        async submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.form.password === '') {
                this.errors.push('Your password is missing')
            }

            if (this.errors.length === 0) {
                await axios
                    .post('/api/login/', this.form)
                    .then(response => {
                        this.userStore.setToken(response.data)

                        console.log(response.data.access)

                        axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access;
                    })
                    .catch(error => {
                        console.log('error', error)
                        this.errors.push('The email or password is incorrect! Or the email is not activated!')
                    })
            }

            if (this.errors.length === 0) {
                await axios
                    .get('/api/me/')
                    .then(response => {
                        this.userStore.setUserInfo(response.data)

                        this.$router.push('/feed')
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }

        }
    }
}
</script>