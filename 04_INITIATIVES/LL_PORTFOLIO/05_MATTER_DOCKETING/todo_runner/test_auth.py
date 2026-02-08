#!/usr/bin/env python3
"""Smoke test for Stage 2.9 — Google OAuth + boundary guard."""

import os
from dotenv import load_dotenv
load_dotenv()

from auth_google import get_drive, get_docs
from boundary import assert_doc_in_approved_folder


def main():
    doc_id = os.environ["LEDGER_DOC_ID"]
    drive = get_drive()
    docs = get_docs()

    assert_doc_in_approved_folder(drive, doc_id)

    doc = docs.documents().get(documentId=doc_id).execute()
    print("AUTH OK.  Ledger title:", doc.get("title"))


if __name__ == "__main__":
    main()
