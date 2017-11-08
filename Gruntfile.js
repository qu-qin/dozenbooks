"use strict";

module.exports = function(grunt) {

	// Load grunt tasks automatically
	require("load-grunt-tasks")(grunt);

	// Time how long tasks take. Can help when optimizing build times
	require("time-grunt")(grunt);

	// Configurable paths for the client
	var clientConfig = {
		app: "public/src",
		bower: "public/src/bower_components",
		build: "public/src/.tmp",
		dist: "public/dist",
		cssDist: "public/dist/css",
		jsDist: "public/dist/js",
		resourceTemplate: "templates/partials/resources/src",
		distResourceTemplate: "templates/partials/resources/dist"
	};

	var emailConfig = {
		host: "smtp.gmail.com",
		port: 25,
		user: "beambook.kindle@gmail.com",
		password: "***********************"
	};

	grunt.initConfig({

		// Project settings
		client: clientConfig,
		email: emailConfig,

		// Watches files for changes and runs tasks based on the changed files
		watch: {
			js: {
				files: ["<%= client.app %>/**/*.js", "!<%= client.bower %>/**/*.js"],
				tasks: ["newer:jshint:all"]
			},
			less: {
				files: ["<%= client.app %>/**/*.less"],
				tasks: ["less:dev"]
			}
		},

		less: {
			dev: {
				files: {
					"<%= client.build %>/app.css": "<%= client.app %>/app.less"
				}
			},
			dist: {
				files: {
					"<%= client.cssDist %>/app.css": ["<%= client.app %>/app.less"]
				}
			}
		},

		jshint: {
			options: {
				jshintrc: ".jshintrc",
				reporter: require("jshint-stylish")
			},
			all: {
				src: [
					"Gruntfile.js",
					"<%= client.app %>/**/*.js",
					"!<%= client.bower %>/**",
					"!<%= client.build %>/**",
					"!<%= client.dist %>/**"
				]
			}
		},

		clean: {
			serve: ".tmp",
			dist: {
				files: [
					{
						dot: true,
						src: [
							"<%= client.build %>",
							"<%= client.dist %>",
							"<%= client.distResourceTemplate %>"
						]
					}
				]
			}
		},

		useminPrepare: {
			html: "<%= client.distResourceTemplate %>/*.html",
			options: {
				dest: "./",
				flow: {
					html: {
						steps: {
							js: ["concat", "uglifyjs"],
							css: ["cssmin"]
						},
						post: {}
					}
				}
			}
		},

		usemin: {
			html: ["<%= client.distResourceTemplate %>/{,*/}*.html"],
			css: ["<%= client.dist %>/**/*.css"],
			js: ["<%= client.dist %>/**/*.js"],
			options: {
				assetsDirs: ["<%= client.dist %>", "<%= client.dist %>/assets"]
			}
		},

		copy: {
			distPrepare: {
				files: [
					{
						expand: true,
						cwd: "<%= client.resourceTemplate %>",
						dest: "<%= client.distResourceTemplate %>",
						src: ["**/*.html"]
					}
				]
			},
			dist: {
				files: [
					{
						expand: true,
						dot: true,
						cwd: "<%= client.app %>",
						dest: "<%= client.dist %>",
						src: [
							"*.{ico,png,txt}",
							"*.html",
							"views/{,*/}*.html",
							"assets/**/*.{webp}",
							"assets/fonts/*"
						]
					},
					{
						expand: true,
						cwd: "<%= client.build %>/assets/images",
						dest: "<%= client.dist %>/assets/images",
						src: ["generated/*"]
					}
				]
			}
		},

		shell: {
			dev: {
				command: "dev_appserver.py app.yaml --host=0.0.0.0 --log_level=debug --smtp_host=<%= email.host %> --smtp_port=<%= email.port %> --smtp_user=<%= email.user %> --smtp_password=<%= email.password %>"
			},
			deploy: {
				command: "appcfg.py --oauth2 update ./"
			}
		},

		concurrent: {
			options: {
				logConcurrentOutput: true
			},
			tasks: ["shell:dev", "watch"]
		}

	});

	grunt.registerTask("serve", "Compile then start a connect web server", function() {

		grunt.task.run([
			"clean:serve",
			"less:dev",
			"concurrent"
		]);

	});

	grunt.registerTask("build", [
		"clean:dist",
		"copy:distPrepare",
		"less:dist",
		"useminPrepare",
		"concat",
		"copy:dist",
		"cssmin",
		"uglify",
		"usemin"
	]);

	grunt.registerTask("deploy", [
		"build",
		"shell:deploy"
	]);

	grunt.registerTask("default", ["serve"]);

};