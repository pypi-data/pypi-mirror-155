from datetime import datetime
from typing import List
from defi_common_lib.model.bundle import Bundle
from defi_common_lib.model.dataset import Dataset
from defi_common_lib.db.database_service import DatabaseService
from defi_common_lib.db.querys import (
    SELECT_PENDING_BUNDLES, SELECT_BUNDLES_DATASETS, UPDATE_BUNDLE_STATUS
)
from constants import Constants


class BundleDao:

    @staticmethod
    def get_pending_bundles() -> List[Bundle]:
        db = DatabaseService()
        bundles = []
        bundles_data = db.get_all_rows(
            sql=SELECT_PENDING_BUNDLES, data=(Constants.PENDING_STATUS)
        )

        if len(bundles_data) > 0:
            for bundle in bundles_data:
                datasets = []
                datasets_data = db.get_all_rows(
                    sql=SELECT_BUNDLES_DATASETS, data=(bundle['bundle_id'])
                )
                for dataset_row in datasets_data:
                    dataset = Dataset(
                        id=dataset_row['dataset_id'],
                        key=dataset_row['key'],
                        source=dataset_row['source']
                    )
                    datasets.append(dataset)

                bundle = Bundle(
                    id=bundle['bundle_id'],
                    created_at=bundle['created_at'],
                    updated_at=bundle['updated_at'],
                    status=bundle['status'],
                    user=bundle['user'],
                    datasets=datasets
                )

                bundles.append(bundle)
        else:
            raise Exception(f'Error retriving pending bundles')

        return bundles

    @staticmethod
    def get_last_bundle() -> Bundle:
        db = DatabaseService()
        bundle = None
        bundle_data = db.get_all_rows(
            sql=SELECT_PENDING_BUNDLES, data=(Constants.PENDING_STATUS)
        )

        if len(bundle_data) > 0:
            bundle = bundle_data[0]
            datasets = []
            datasets_data = db.get_all_rows(
                sql=SELECT_BUNDLES_DATASETS, data=(bundle['bundle_id'])
            )
            for dataset_row in datasets_data:
                dataset = Dataset(
                    id=dataset_row['dataset_id'],
                    key=dataset_row['key'],
                    source=dataset_row['source'],
                    file_name=dataset_row['file_name']
                )
                datasets.append(dataset)

            bundle = Bundle(
                id=bundle['bundle_id'],
                created_at=bundle['created_at'],
                updated_at=bundle['updated_at'],
                status=bundle['status'],
                user=bundle['user'],
                price=bundle['price'],
                datasets=datasets
            )

        return bundle

    @staticmethod
    def update_status(id: str, status: str, updated_at: datetime, did: str):
        db = DatabaseService()
        db.execute(
            sql=UPDATE_BUNDLE_STATUS,
            data=(status, updated_at, did, id)
        )
