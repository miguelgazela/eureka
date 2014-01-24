module.exports = function(grunt) {

    // 1. All configuration goes here 
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        concat: {
            dist: {
                src: [
                    'eureka/ideas/static/ideas/js/*.js' // All JS files in the JS folder
                ],
                dest: 'eureka/ideas/static/ideas/js/build/production.js',
            }
        },

        uglify: {
            build: {
                src: 'eureka/ideas/static/ideas/js/build/production.js',
                dest: 'eureka/ideas/static/ideas/js/build/production.min.js'
            }
        },

        imagemin: {
            dynamic: {
                files: [{
                    expand: true,
                    cwd: 'eureka/ideas/static/ideas/images/',
                    src: ['**/*.{png,jpg,gif}'],
                    dest: 'eureka/ideas/static/ideas/images/build/'
                }]
            }
        },

        watch: {
            options: {
                livereload: true,
            },
            scripts: {
                files: ['eureka/ideas/static/ideas/js/*.js'],
                tasks: ['concat', 'uglify'],
                options: {
                    spawn: false,
                },
            },
            css: {
                files: ['eureka/ideas/static/ideas/css/*.scss'],
                tasks: ['sass'],
                options: {
                    spawn: false,
                },
            },
        },

        sass: {
            dist: {
                options: {
                    style: 'compressed'
                },
                files: {
                    'eureka/ideas/static/ideas/css/build/global.css': 'eureka/ideas/static/ideas/css/global.scss'
                }
            }
        }
    });

    // 3. Where we tell Grunt we plan to use this plug-in.
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-imagemin');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-sass');

    // 4. Where we tell Grunt what to do when we type "grunt" into the terminal.
    grunt.registerTask('default', ['concat', 'uglify', 'imagemin', 'sass', 'watch']);

};