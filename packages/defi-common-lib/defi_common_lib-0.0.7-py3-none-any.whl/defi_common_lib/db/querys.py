# Get the agent
SELECT_AGENT = (
    "SELECT agent_id, category, subcategory FROM agent_config "
    "WHERE agent_id = %s "
)


# Get the different protocols associated with an agent and it's state
SELECT_AGENT_STATE = (
    "SELECT agent_state.agent_id, protocols.protocol_id, protocols.name, "
    "protocols.chain, protocols.version, agent_protocols.periodicity, "
    "agent_state.last_updated, agent_state.last_entry, reports.price "
    "FROM agent_state, protocols, agent_protocols, reports "
    "WHERE agent_state.agent_id = %s "
    "AND agent_state.protocol_id= protocols.protocol_id "
    "AND agent_state.protocol_id = agent_protocols.protocol_id "
    "AND agent_state.agent_id = agent_protocols.agent_id "
    "AND agent_state.agent_id = reports.agent_id "
)


# Get the different agents with a configuration related to a specific protocol
SELECT_AGENT_PROTOCOLS = (
    "SELECT DISTINCT agent_id FROM protocols, agent_protocols "
    "WHERE agent_protocols.protocol_id = protocols.protocol_id AND protocols.name = %s "
)


# Updates the agent state with the last processed day and entry
UPDATE_AGENT_STATE = (
    "UPDATE agent_state set last_updated = %s, last_entry = %s "
    "WHERE agent_id = %s and protocol_id= %s"
)

SELECT_PENDING_BUNDLES = (
    "SELECT bundles.bundle_id, bundles.created_at, bundles.updated_at, "
    "bundles.`user`, bundles.status, bundles.price  "
    "FROM bundles "
    "WHERE bundles.status = %s "
    "ORDER BY created_at DESC "
)

SELECT_LAST_BUNDLE = (
    "SELECT bundles.bundle_id, bundles.created_at, bundles.updated_at, "
    "bundles.`user`, bundles.status, bundles.price "
    "FROM bundles "
    "WHERE bundles.status = %s "
    "ORDER BY created_at ASC "
    "LIMIT 1"
)

SELECT_BUNDLES_DATASETS = (
    "SELECT datasets.dataset_id,datasets.`key`, datasets.source, datasets.file_name "
    "FROM datasets, dataset_bundles "
    "WHERE datasets.dataset_id = dataset_bundles.dataset_dataset_id "
    "AND dataset_bundles.bundle_bundle_id = %s "
)

UPDATE_BUNDLE_STATUS = (
    "UPDATE bundles "
    "SET bundles.status = %s, bundles.updated_at = %s, bundles.did = %s "
    "WHERE bundles.bundle_id = %s"
)
