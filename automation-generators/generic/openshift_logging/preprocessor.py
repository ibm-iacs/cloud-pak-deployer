from generatorPreProcessor import GeneratorPreProcessor
import sys

# Validating:
# ---
# openshift_logging:
# - openshift_cluster_name: "{{ env_id }}"
#   configure_es_log_store: False
#   cluster_wide_logging:
#   - input: application
#     logging_name: loki-application
#     labels:
#       cluster_name: "{{ env_id }}"
#   - input: infrastructure
#     logging_name: loki-application
#     labels:
#       cluster_name: "{{ env_id }}"
#   - input: audit
#     logging_name: loki-audit
#     labels:
#       cluster_name: "{{ env_id }}"
#   logging_output:
#   - name: loki-application
#     type: loki
#     url: https://loki-application.sample.com
#     certificates:
#       cert: "{{ env_id }}"-loki-cert
#       key: "{{ env_id }}"-loki-key
#       ca: "{{ env_id }}"-loki-ca
#   - name: loki-audit
#     type: loki
#     url: https://loki-audit.sample.com
#     certificates:
#       cert: "{{ env_id }}"-loki-cert
#       key: "{{ env_id }}"-loki-key
#       ca: "{{ env_id }}"-loki-ca

def preprocessor(attributes=None, fullConfig=None):
    g = GeneratorPreProcessor(attributes,fullConfig)

    g('openshift_cluster_name').isRequired()

    # Now that we have reached this point, we can check the attribute details if the previous checks passed
    if len(g.getErrors()) == 0:
        fc = g.getFullConfig()
        ge=g.getExpandedAttributes()

        if 'configure_es_log_store' in ge:
            if type(ge['configure_es_log_store']) != bool:
                g.appendError(msg='Attribute configure_es_log_store must be either true or false if specified. Default is false.')

        if 'cluster_wide_logging' in ge:
            for cwl in ge['cluster_wide_logging']:
                if 'logging_name' in cwl:
                    if not 'logging_output' in ge:
                        g.appendError(msg='If logging_name specified for cluster_wide_logging, the logging_output entry must be added with the associated name')
                    else:
                        logging_name_found=False
                        for lo in ge['logging_output']:
                            if 'name' in lo and lo['name']==cwl['logging_name']:
                                logging_name_found=True
                        if not logging_name_found:
                            g.appendError(msg='logging_output entry with name '+cwl['logging_name']+' was not found')

        if 'logging_output' in ge:
            for lo in ge['logging_output']:
                if "name" not in lo:
                    g.appendError(msg='Attribute name must be specified for all logging_output entries')
                if "type" not in lo:
                    g.appendError(msg='Attribute type must be specified for all logging_output entries')
                elif lo['type'] != "loki":
                    g.appendError(msg='Type of logging_output entry must be one of: loki')
                if "url" not in lo:
                    g.appendError(msg='Attribute url must be specified for all logging_output entries')
                if "certificates" in lo:
                    loc=lo['certificates']
                    if "cert" not in loc:
                        g.appendError(msg='Certificate must be specified for logging_output certificates')
                    if "key" not in loc:
                        g.appendError(msg='Key must be specified for logging_output certificates')
                    if "ca" not in loc:
                        g.appendError(msg='CA bundle must be specified for logging_output certificates')
    result = {
        'attributes_updated': g.getExpandedAttributes(),
        'errors': g.getErrors()
    }
    return result