<template>
    <div class="mx-auto max-w-7xl grid grid-cols-2 gap-4">
        <div class="main-left cols-span-1 bg-white rounded-lg border-gray-300 px-10 py-12 space-y-8">
            <h2 class="text-2xl font-semibold">Sign up</h2>
            <p class="text-gray-500">Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                Lorem ipsum dolor sit
                mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.</p>
            <p class="font-bold">Don't have an account? <RouterLink :to="{ 'name': 'login' }" class="underline">Click here
                </RouterLink> to create one!</p>
        </div>
        <div class="main-right cols-span-1 bg-white rounded-lg border-gray-300 px-10 py-12">
            <form action="" class="space-y-5" v-on:submit.prevent="submitForm">
                <div>
                    <label>Name</label><br>
                    <input type="text" v-model="form.name" placeholder="Your full name"
                        class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                </div>

                <div>
                    <label>E-mail</label><br>
                    <input type="email" v-model="form.email" placeholder="Your e-mail address"
                        class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                </div>

                <div>
                    <label>Password</label><br>
                    <input type="password" v-model="form.password1" placeholder="Your password"
                        class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                </div>

                <div>
                    <label>Repeat password</label><br>
                    <input type="password" v-model="form.password2" placeholder="Repeat your password"
                        class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                </div>

                <template v-if="errors.length > 0">
                    <div class="bg-red-300 text-white rounded-lg p-6">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>
                </template>


                <button type="submit" class="p-4 bg-purple-500 text-white rounded-lg">Submit</button>



            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

import { useToastStore } from '@/stores/toast'

export default {
    setup() {
        const toastStore = useToastStore()

        return {
            toastStore
        }
    },

    data() {
        return {
            form: {
                email: '',
                name: '',
                password1: '',
                password2: ''
            },
            errors: [],
        }
    },

    methods: {
        submitForm() {
            this.errors = []

            if (this.form.email === '') {
                this.errors.push('Your e-mail is missing')
            }

            if (this.form.name === '') {
                this.errors.push('Your name is missing')
            }

            if (this.form.password1 === '') {
                this.errors.push('Your password is missing')
            }

            if (this.form.password1 !== this.form.password2) {
                this.errors.push('The password does not match')
            }

            if (this.errors.length === 0) {
                axios
                    .post('/api/signup/', this.form)
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'The user is registered. Please activate your account by clicking your email link!', 'bg-emerald-500')

                            this.form.email = ''
                            this.form.name = ''
                            this.form.password1 = ''
                            this.form.password2 = ''
                        } else {
                            const data = JSON.parse(response.data.message)
                            // console.log('data', data);
                            // console.log('response.data.message', response.data.message);
                            for (const key in data) {

                                this.errors.push(data[key][0].message)
                            }

                            this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red-300')
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }
        }
    }
}
</script>
