#Crea columna id y lo lleva a la primera posición

df["id"] = ["id_man_" + str(i) for i in range(1, len(df) + 1)]

columna_extraida_ = df.pop("id")

df.insert(0, "id", columna_extraida_)



#Nueva columna con el nombre de la empresa a partir de la url y la mueve a la segunda posición

df["empresa"] = df["url"].apply(lambda x: x.split("/")[-1].split("-")[0])

columna_extraida = df.pop("empresa")

df.insert(1, "empresa", columna_extraida)



#Elimina "tecnologias_Tecnologías_" de todos los nomnbres de columna

df.columns = df.columns.str.replace("tecnologias_Tecnologías_", "", regex=False)



#Renombra columnas que empiezan por detalles_1_, detalles_2_

df = df.rename(columns={"detalles_1_SALARIO" : "Salario", "detalles_1_PRESENCIAL" : "Presencial", "detalles_1_TELETRABAJO" : "Teletrabajo", "detalles_1_REMOTO" : "Remoto", "detalles_2_DÍA LABORABLE" : "dia_laborable", "detalles_2_VACACIONES" : "vacaciones", "detalles_2_JORNADA LABORAL" : "jornada_laboral", "detalles_2_TURNO CONTINUO" : "turno_continuo", "detalles_1_VARIABLE" : "variable"})



#Quitar " DÍAS" en columna vacaciones
###Pendiente revisar ILIMITADO

df["vacaciones"] = df["vacaciones"].str.replace(" DÍAS", "")

df["vacaciones"].value_counts()



#Columna habilidades_Otras habilidades. 

# Convierte los strings a listas.
import ast
df["habilidades_Otras habilidades"] = df["habilidades_Otras habilidades"].apply(ast.literal_eval)

#Crea una lista con las habilidades únicas
todas_habilidades = sum(df["habilidades_Otras habilidades"], [])
habilidades_unicas = list(set(todas_habilidades))

# Crea una columna para cada habilidad única y usa la columna original para poblar las nuevas conlumnas con 1 o 0
for habilidad in habilidades_unicas:
    df[habilidad] = df["habilidades_Otras habilidades"].apply(lambda x: 1 if habilidad in x else 0)

#Elimina la columna habilidades_Otras habilidades. 

df = df.drop("habilidades_Otras habilidades", axis = 1)

#Dividimos las columnas en 3 categorías y generamos un df para cada uno de ellos.

programas = ["id", "Python", "C++", "Cinema 4D", "CRM", "Canva", "Trello", "Google Analytics", "Adobe Photoshop", 
    "Adobe Illustrator", "WordPress", "Java", "SQL", "SOAP", "OpenApi", "JavaScript", "Cobol", 
    "C#", ".NET", "JSON", "Angular2+", "Microsoft Excel", "Hubspot", "AWS", "Kafka", "Argo CD", 
    "Flux", "React", "Kotlin", "Swift", "PostgreSQL", "Spring", "Azure", "Kubernetes", "Terraform", 
    "Docker", "Linux", "Git", "Golang", "Rust", "GitLab", "Django", "Celery", "Fastapi", "MySQL", 
    "NodeJS", "TypeScript", "MVC", "dbt", "Google Cloud", "Airflow", "z/OS", "DB2", "PowerShell", 
    "Bash", "Magento", "Prestashop", "BigCommerce", "Salesforce", "Shopify", "WooCommerce", 
    "RabbitMQ", "NextJS", "Tailwind", "Jenkins", "Databricks", "Prometheus", "Google Sheets", "nestJS", 
    "Vue", "MQTT", "Express", "Koa", "Spring Boot", "Go", "Bootstrap", "Pytest", "Github", "PHP", 
    "Symfony", "Figma", "HTML", "CSS", "Jest", "Hibernate", "API", "WebSockets", "Svelte", "BigQuery", 
    "Redux", "Ansible", "SQLServer", "Visual Studio", "REST", "ETL", "S3", "Redshift", "Snowflake", 
    "Auth0", "Tableau", "IIS", "Pulumi", "Azure DevOps", "Laravel", "Yii", "AWS ECS", "Nest", "PySpark", 
    "AWS Lambda", "Selenium", "Appium", "Cypress", "RxJS", "Clojure", "Grafana", "ELK", "Spark", "Jmeter", 
    "Gatling", "Apple iOS", "SwiftUI", "XCTest", "UIKit", "Atlassian", "Groovy", "ServiceNow", "Ethereum", 
    "Web3", ".Net Core", "Swagger", "Helm", "Datadog", "Kong", "Quarkus", "Vitest", "TestingLibrary", 
    "Metabase", "Webpack", "Elasticsearch", "Dart", "Flutter", "Blender", "Ruby on Rails", "Citrix", 
    "Windows", "VMWare", "Hyper-v", "Xen", "R", "Three.js", "MongoDB", "React Native", "Jira", "NoSQL", 
    "Scrapy", "Apache Beam", "Nagios", "Zabbix", "DNS", "HTTP4s", "Razor", "Shiny", "Xray", "AWS Cloudwatch", 
    "Google Ads", "Pipedrive", "Notion", "Monday", "DialogFlow", "GraphQL", "jQuery", "AngularJS", "Ionic", 
    "Viper", "Android", "Slack", "Mocha", "junit4", "Amplitude", "Mixpanel", "DynamoDB", "SaaS", "Redis", 
    "KVM", "Solr", "Flask", "Sklearn", "Google Looker Studio", "Scala", "Gitflow", "ASP.net", "Pandas", 
    "Numpy", "Google Firebase", "Riverpod", "gRPC", "Protobuf", "PHPunit", "Drupal", "Zoho", "Fortran", 
    "Vite", "TensorFlow", "ActiveMQ", "Cisco", "Microsoft Sharepoint", "Microsoft Dynamics 365", "Cassandra", 
    "Dagger2", "Core Data", "Ruby", "PyTorch", "AWS SageMaker", "Oracle", "Microsoft Power BI", 
    "Google Tag Manager", "Maven", "JUnit", "Blazor", "Microsoft", "javacript", "Sketch", "Adobe Xd", 
    "Axure", "InfluxDB", "Flink", "Postman", "JBoss", "Transact-SQL (T-SQL)", "PL/SQL", "Cordova", 
    "BlueTooth", "Nuxt.js", "Babel", "Microsoft Office 365", "Objective-C", "OpenCV", "Jasmine", 
    "Productboard", "Github Actions", "openlayers", "CARTO", "ArcGIS", "Leaflet", "Geoserver", "Google AdManager", 
    "Google Data Studio", "Google Optimize", "Couchbase", "Elixir", "Adobe Premiere Pro", "Cucumber", 
    "Sagas", "Apollo", "MVVM", "ClickHouse", "Micronaut Framework", "Airtable", "Asana", "Specflow", "Puppeteer", 
    "Miro", "Backbone", "CMS", "KendoUI", "Adobe Suit", "Apache", "Karate", "PACT", "MariaDB", "TestNg", 
    "AWS-User", "Apple macOS", "Microsoft Active Directory", "Storybook", "Keycloak", "slq-server", "GraalVM", 
    "FlexBox", "Unix", "data-lake", "shell-scripting", "postgres", "rabbit", "reactive-programming", "Puppet", 
    "Unity3D", "SAP", "Nginx", "Invision", "Chef", "Hotjar", "LookBack", "Maze", "Webflow", "CMake", "Qt", 
    "Alfresco", "MapBox", "ChartJS", "Google Maps", "OpenGL", "UML", "Genesys", "SIP", "Vuex", "VanillaJS", 
    "Hadoop", "OpenShift", "Hazelcast", "Android Studio", "PowerCenter", "Microsoft SQL Integration Services (SSIS)", 
    "Sass", "Ember", "Entity", "CodeIgniter", "OpenStack", "NgRx", "WPF", "FlaUI", "Gherkin", "Playwright", 
    "SonarQube", "Nexus", "Fortinet", "Vagrant", "F5", "Aruba", "Infoblox", "Palo Alto", "Zscaler", "MobileIron", 
    "PRTG", "VMware NSX", "WebComponents", "New Relic", "Confluence", "Plesk", "AJAX", "SCADA", "Kibana", 
    "Microstrategy", "BI", "Adobe Analytics", "Adobe Campaign", "Selligent", "screen-scraping", "TestFlight", 
    "Odoo", "WebApi", "RollupJS", "YAML", "Lucene", "RedHat", "Segment", "Facebook Ads", "Linkedin Ads", 
    "Bitbucket", "Lua", "Zend", "CircleCI", "Serverless", "Zapier", "Apache Tomcat", "git-bash"]

habilidades = ["id", "Pensamiento creativo", "Tolerancia a la incertidumbre", "Resistencia a la frustración", 
    "Comunicación verbal", "Capacidad de escucha", "Capacidad de mentorización", "Capacidad de dar feedback", 
    "Adaptabilidad al cambio", "Visión estratégica", "Proactividad", "Capacidad de recibir feedback", 
    "Trabajo en equipo", "Habilidades de negociación", "Liderazgo", "Atención al detalle", 
    "Inteligencia emocional", "Capacidad de abstracción", "Capacidad de presentación", "Comunicación escrita", 
    "Pensamiento analítico", "Comunicación intercultural", "Autonomía en el aprendizaje", "Capacidad de autogestión", 
    "Aprendizaje Continuo", "Gestión de equipo", "Visión crítica"]


general = ["id", "empresa", "url", "fecha_extraccion", "titulo", "oferta_activada", "Salario", "Presencial", 
    "Teletrabajo", "dia_laborable", "vacaciones", "jornada_laboral", "variable", "turno_continuo", "Remoto"]




programas_df = df[programas]

habilidades_df = df[habilidades]

#Poblamos programas_df con boolenos en función de lo que la oferta solicita

programas_df.loc[:,programas_df.columns != "id"] = programas_df.loc[:,programas_df.columns != "id"].fillna(0)
programas_df.loc[:,programas_df.columns != "id"] = programas_df.loc[:,programas_df.columns != "id"].map(lambda x: 1 if x != 0 else 0)


#Sacamos los emojis de la columna titulo

import emoji

general_df["titulo"] = general_df["titulo"].apply(lambda x: emoji.replace_emoji(x, replace='')) 

#Modificamos la columna oferta activada a booleanos

general_df["oferta_activada"] = general_df["oferta_activada"].apply(lambda x: 1 if x == "Activa" else 0)

#Limpieza columna Salario

general_df["Salario"] =  general_df["Salario"].str.replace("DESDE €", "").str.replace("HASTA €","").str.replace("€","").str.replace("K","")

general_df["Salario"] = general_df["Salario"].str.replace(r".*-\s*", "", regex=True).str.replace("HASTA \u202f", "").str.replace("HASTA US$", "")

general_df["Salario"] = general_df["Salario"].astype("float")

#Limpieza columna turno_continuo  

general_df["turno_continuo"] = general_df["turno_continuo"].apply(lambda x : "No" if pd.isna(x) else x)

#Limpieza de variable y la lleva hasta la posición 7, al lado de sueldo

general_df["variable"] = general_df["variable"].str.replace("+€","").str.replace("K","").str.replace("+\u202f€","").str.replace(",",".").astype("float")
general_df["variable"] = general_df["variable"].fillna(0)


columna_variable_extraida = general_df.pop("variable")

general_df.insert(7, "variable", columna_variable_extraida)

#Basandose en las columnas teletrabajo y Remoto actualizamos la columna teletrabajo con el porcentaje de teletrabajo
#Que permite la oferta
#Drop de la columna remoto

general_df["Teletrabajo"] = general_df.apply(lambda x : "100%" if pd.isna(x ["Teletrabajo"]) and x["Remoto"] == "100%" else ("0" if pd.isna(x['Teletrabajo']) and pd.isna(x['Remoto']) else x['Teletrabajo']), axis=1)

general_df["Teletrabajo"] = general_df["Teletrabajo"].str.replace("%","").astype("int")

general_df = general_df.drop("Remoto", axis = 1)